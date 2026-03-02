from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime, timedelta
import logging
from logging.handlers import RotatingFileHandler
import requests

try:
    import pytesseract
    HAS_PYTESSERACT = True
except ImportError:
    HAS_PYTESSERACT = False
from PIL import Image
import numpy as np
from io import BytesIO
import base64
import sqlite3

app = Flask(__name__)

# Configuration from environment variables with defaults
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB max file size
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///odds_history.db')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
app.config['JSON_SORT_KEYS'] = False

# Request validation constants
MAX_PROMPT_LENGTH = 5000  # Max characters in API prompt
MIN_ODDS_VALUE = 1.01
MAX_ODDS_VALUE = 99.99

db = SQLAlchemy(app)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

# Setup logging
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/odds_predictor.log', maxBytes=10240000, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Football Odds Predictor started')
else:
    logging.basicConfig(level=logging.DEBUG)

# Initialize database
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Database Model
class OddsRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_name = db.Column(db.String(200))
    home_team = db.Column(db.String(100))  # Home team name
    away_team = db.Column(db.String(100))  # Away team name
    league = db.Column(db.String(100))  # Premier League, La Liga, Serie A, Bundesliga, Ligue 1
    odds_1 = db.Column(db.Float)  # Home win
    odds_x = db.Column(db.Float)  # Draw
    odds_2 = db.Column(db.Float)  # Away win
    source = db.Column(db.String(50))  # Betpawa or 1xbet
    image_path = db.Column(db.String(300))
    uploaded_at = db.Column(db.DateTime, default=datetime.now)
    actual_result = db.Column(db.String(1))  # '1', 'X', or '2' - actual match outcome
    is_completed = db.Column(db.Boolean, default=False)  # True if result is uploaded
    notes = db.Column(db.Text)
    btts = db.Column(db.String(1))  # 'Y' or 'N' - Both Teams To Score
    goals_for = db.Column(db.Integer)  # Total goals in match (for BTTS tracking)

def init_sample_data():
    """Initialize database with sample matches if empty"""
    try:
        # Only add sample data if database is empty
        if OddsRecord.query.count() == 0:
            sample_matches = [
                # ============ UPCOMING MATCHES (MAIN FOCUS) ============
                
                # Premier League Upcoming
                {'home_team': 'Arsenal', 'away_team': 'Liverpool', 'league': 'Premier League',
                 'odds_1': 2.25, 'odds_x': 3.40, 'odds_2': 3.10, 'source': 'Betpawa',
                 'is_completed': False, 'uploaded_at': datetime.now()},
                {'home_team': 'Manchester City', 'away_team': 'Chelsea', 'league': 'Premier League',
                 'odds_1': 1.80, 'odds_x': 3.80, 'odds_2': 4.20, 'source': 'Betpawa',
                 'is_completed': False, 'uploaded_at': datetime.now()},
                {'home_team': 'Manchester United', 'away_team': 'Tottenham', 'league': 'Premier League',
                 'odds_1': 2.10, 'odds_x': 3.50, 'odds_2': 3.40, 'source': '1xbet',
                 'is_completed': False, 'uploaded_at': datetime.now()},
                {'home_team': 'Newcastle', 'away_team': 'Brighton', 'league': 'Premier League',
                 'odds_1': 1.95, 'odds_x': 3.65, 'odds_2': 3.85, 'source': 'Betpawa',
                 'is_completed': False, 'uploaded_at': datetime.now()},
                {'home_team': 'Aston Villa', 'away_team': 'West Ham', 'league': 'Premier League',
                 'odds_1': 2.05, 'odds_x': 3.55, 'odds_2': 3.75, 'source': '1xbet',
                 'is_completed': False, 'uploaded_at': datetime.now()},
                
                # La Liga Upcoming
                {'home_team': 'Barcelona', 'away_team': 'Real Madrid', 'league': 'La Liga',
                 'odds_1': 2.10, 'odds_x': 3.50, 'odds_2': 3.30, 'source': 'Betpawa',
                 'is_completed': False, 'uploaded_at': datetime.now()},
                {'home_team': 'Atletico Madrid', 'away_team': 'Valencia', 'league': 'La Liga',
                 'odds_1': 1.95, 'odds_x': 3.65, 'odds_2': 3.85, 'source': '1xbet',
                 'is_completed': False, 'uploaded_at': datetime.now()},
                {'home_team': 'Sevilla', 'away_team': 'Real Betis', 'league': 'La Liga',
                 'odds_1': 2.20, 'odds_x': 3.40, 'odds_2': 3.35, 'source': 'Betpawa',
                 'is_completed': False, 'uploaded_at': datetime.now()},
                {'home_team': 'Athletic Bilbao', 'away_team': 'Real Sociedad', 'league': 'La Liga',
                 'odds_1': 2.05, 'odds_x': 3.50, 'odds_2': 3.60, 'source': '1xbet',
                 'is_completed': False, 'uploaded_at': datetime.now()},
                
                # Serie A Upcoming
                {'home_team': 'Juventus', 'away_team': 'AC Milan', 'league': 'Serie A',
                 'odds_1': 2.30, 'odds_x': 3.35, 'odds_2': 3.00, 'source': 'Betpawa',
                 'is_completed': False, 'uploaded_at': datetime.now()},
                {'home_team': 'Inter Milan', 'away_team': 'AS Roma', 'league': 'Serie A',
                 'odds_1': 1.70, 'odds_x': 4.00, 'odds_2': 4.80, 'source': '1xbet',
                 'is_completed': False, 'uploaded_at': datetime.now()},
                {'home_team': 'Napoli', 'away_team': 'Lazio', 'league': 'Serie A',
                 'odds_1': 2.15, 'odds_x': 3.50, 'odds_2': 3.35, 'source': 'Betpawa',
                 'is_completed': False, 'uploaded_at': datetime.now()},
                {'home_team': 'Atalanta', 'away_team': 'Fiorentina', 'league': 'Serie A',
                 'odds_1': 1.90, 'odds_x': 3.55, 'odds_2': 4.20, 'source': '1xbet',
                 'is_completed': False, 'uploaded_at': datetime.now()},
                
                # Bundesliga Upcoming
                {'home_team': 'Bayern Munich', 'away_team': 'Borussia Dortmund', 'league': 'Bundesliga',
                 'odds_1': 1.65, 'odds_x': 4.20, 'odds_2': 5.50, 'source': 'Betpawa',
                 'is_completed': False, 'uploaded_at': datetime.now()},
                {'home_team': 'RB Leipzig', 'away_team': 'Bayer Leverkusen', 'league': 'Bundesliga',
                 'odds_1': 2.20, 'odds_x': 3.50, 'odds_2': 3.25, 'source': '1xbet',
                 'is_completed': False, 'uploaded_at': datetime.now()},
                {'home_team': 'VfB Stuttgart', 'away_team': 'Eintracht Frankfurt', 'league': 'Bundesliga',
                 'odds_1': 1.95, 'odds_x': 3.65, 'odds_2': 3.90, 'source': 'Betpawa',
                 'is_completed': False, 'uploaded_at': datetime.now()},
                {'home_team': 'Union Berlin', 'away_team': 'Borussia M\'gladbach', 'league': 'Bundesliga',
                 'odds_1': 2.15, 'odds_x': 3.45, 'odds_2': 3.50, 'source': '1xbet',
                 'is_completed': False, 'uploaded_at': datetime.now()},
                
                # Ligue 1 Upcoming
                {'home_team': 'PSG', 'away_team': 'Marseille', 'league': 'Ligue 1',
                 'odds_1': 1.40, 'odds_x': 5.00, 'odds_2': 9.00, 'source': 'Betpawa',
                 'is_completed': False, 'uploaded_at': datetime.now()},
                {'home_team': 'Monaco', 'away_team': 'Lyon', 'league': 'Ligue 1',
                 'odds_1': 2.10, 'odds_x': 3.50, 'odds_2': 3.60, 'source': '1xbet',
                 'is_completed': False, 'uploaded_at': datetime.now()},
                {'home_team': 'Lille', 'away_team': 'Nice', 'league': 'Ligue 1',
                 'odds_1': 2.05, 'odds_x': 3.30, 'odds_2': 3.75, 'source': 'Betpawa',
                 'is_completed': False, 'uploaded_at': datetime.now()},
                {'home_team': 'Lens', 'away_team': 'Rennes', 'league': 'Ligue 1',
                 'odds_1': 2.15, 'odds_x': 3.40, 'odds_2': 3.50, 'source': '1xbet',
                 'is_completed': False, 'uploaded_at': datetime.now()},
                
                # Champions League Upcoming
                {'home_team': 'Real Madrid', 'away_team': 'Manchester City', 'league': 'Champions League',
                 'odds_1': 2.50, 'odds_x': 3.30, 'odds_2': 2.80, 'source': 'Betpawa',
                 'is_completed': False, 'uploaded_at': datetime.now()},
                {'home_team': 'Bayern Munich', 'away_team': 'Arsenal', 'league': 'Champions League',
                 'odds_1': 2.00, 'odds_x': 3.50, 'odds_2': 3.60, 'source': '1xbet',
                 'is_completed': False, 'uploaded_at': datetime.now()},
                {'home_team': 'Inter Milan', 'away_team': 'Atletico Madrid', 'league': 'Champions League',
                 'odds_1': 1.95, 'odds_x': 3.60, 'odds_2': 3.80, 'source': 'Betpawa',
                 'is_completed': False, 'uploaded_at': datetime.now()},
                {'home_team': 'PSG', 'away_team': 'Barcelona', 'league': 'Champions League',
                 'odds_1': 2.40, 'odds_x': 3.35, 'odds_2': 2.85, 'source': '1xbet',
                 'is_completed': False, 'uploaded_at': datetime.now()},
                
                # ============ PAST MATCHES (JUST A FEW FOR REFERENCE) ============
                
                {'home_team': 'Liverpool', 'away_team': 'Chelsea', 'league': 'Premier League',
                 'odds_1': 2.15, 'odds_x': 3.40, 'odds_2': 3.50, 'actual_result': '1',
                 'source': 'Betpawa', 'is_completed': True, 'btts': 'Y', 'goals_for': 3,
                 'uploaded_at': datetime.now() - timedelta(days=2)},
                {'home_team': 'Real Madrid', 'away_team': 'Barcelona', 'league': 'La Liga',
                 'odds_1': 2.00, 'odds_x': 3.60, 'odds_2': 3.40, 'actual_result': 'X',
                 'source': '1xbet', 'is_completed': True, 'btts': 'Y', 'goals_for': 2,
                 'uploaded_at': datetime.now() - timedelta(days=3)},
                {'home_team': 'Inter Milan', 'away_team': 'AC Milan', 'league': 'Serie A',
                 'odds_1': 2.10, 'odds_x': 3.30, 'odds_2': 3.50, 'actual_result': '1',
                 'source': 'Betpawa', 'is_completed': True, 'btts': 'Y', 'goals_for': 3,
                 'uploaded_at': datetime.now() - timedelta(days=4)},
                {'home_team': 'Bayern Munich', 'away_team': 'RB Leipzig', 'league': 'Bundesliga',
                 'odds_1': 1.75, 'odds_x': 3.80, 'odds_2': 4.80, 'actual_result': '1',
                 'source': '1xbet', 'is_completed': True, 'btts': 'Y', 'goals_for': 4,
                 'uploaded_at': datetime.now() - timedelta(days=5)},
                {'home_team': 'PSG', 'away_team': 'Marseille', 'league': 'Ligue 1',
                 'odds_1': 1.45, 'odds_x': 4.80, 'odds_2': 7.50, 'actual_result': '1',
                 'source': 'Betpawa', 'is_completed': True, 'btts': 'Y', 'goals_for': 2,
                 'uploaded_at': datetime.now() - timedelta(days=6)},
            ]
            
            for match_data in sample_matches:
                match_name = f"{match_data['home_team']} vs {match_data['away_team']}"
                match = OddsRecord(match_name=match_name, **match_data)
                db.session.add(match)
            
            db.session.commit()
            app.logger.info(f"✓ Initialized database with {len(sample_matches)} sample matches")
    except Exception as e:
        app.logger.error(f"Error initializing sample data: {str(e)}")
        db.session.rollback()

with app.app_context():
    db.create_all()
    init_sample_data()
    # Update with live upcoming fixtures from web
    try:
        from fetch_live_fixtures import update_live_fixtures
        update_live_fixtures()
    except Exception as e:
        app.logger.warning(f"Could not fetch live fixtures: {e}")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def categorize_odds(odds_value):
    """
    Categorize odds into ranges for historical analysis
    Returns: (category_name, min_range, max_range)
    """
    if odds_value <= 1.25:
        return ("Very Heavy Favorite", 1.01, 1.25)
    elif odds_value <= 1.50:
        return ("Heavy Favorite", 1.26, 1.50)
    elif odds_value <= 1.80:
        return ("Favorite", 1.51, 1.80)
    elif odds_value <= 2.20:
        return ("Slight Favorite", 1.81, 2.20)
    elif odds_value <= 3.00:
        return ("Underdog", 2.21, 3.00)
    elif odds_value <= 4.50:
        return ("Heavy Underdog", 3.01, 4.50)
    elif odds_value <= 7.00:
        return ("Very Heavy Underdog", 4.51, 7.00)
    else:
        return ("Extreme Underdog", 7.01, 99.99)

def analyze_odds_range(odds_value, bet_type='1'):
    """
    Analyze historical data for similar odds ranges with comprehensive metrics
    Returns: win_rate, upset_rate, btts_rate, confidence, sample_size
    
    bet_type: '1' (home), 'X' (draw), '2' (away)
    """
    category, min_odd, max_odd = categorize_odds(odds_value)
    
    # Get all completed matches with this bet type odds in similar range
    if bet_type == '1':
        matches = OddsRecord.query.filter(
            OddsRecord.is_completed == True,
            OddsRecord.odds_1 >= min_odd,
            OddsRecord.odds_1 <= max_odd,
            OddsRecord.actual_result.isnot(None)
        ).all()
        result_marker = '1'
    elif bet_type == 'X':
        matches = OddsRecord.query.filter(
            OddsRecord.is_completed == True,
            OddsRecord.odds_x >= min_odd,
            OddsRecord.odds_x <= max_odd,
            OddsRecord.actual_result.isnot(None)
        ).all()
        result_marker = 'X'
    else:  # bet_type == '2'
        matches = OddsRecord.query.filter(
            OddsRecord.is_completed == True,
            OddsRecord.odds_2 >= min_odd,
            OddsRecord.odds_2 <= max_odd,
            OddsRecord.actual_result.isnot(None)
        ).all()
        result_marker = '2'
    
    if not matches:
        return {
            'category': category,
            'win_rate': 0,
            'upset_rate': 0,
            'btts_rate': 0,
            'confidence': 0,
            'sample_size': 0,
            'is_favorite': odds_value <= 2.50
        }
    
    total = len(matches)
    wins = len([m for m in matches if m.actual_result == result_marker])
    losses = total - wins
    btts_yes = len([m for m in matches if m.btts == 'Y'])
    btts_recorded = len([m for m in matches if m.btts in ['Y', 'N']])
    
    # Determine if this odds range represents favorite or underdog
    is_favorite = odds_value <= 2.50
    
    # Calculate key metrics
    win_rate = round((wins / total) * 100, 1)
    loss_rate = round((losses / total) * 100, 1)
    
    # For favorites: upset rate = how often they LOSE
    # For underdogs: upset rate = how often they WIN (pull off an upset)
    upset_rate = loss_rate if is_favorite else win_rate
    
    btts_rate = round((btts_yes / btts_recorded) * 100, 1) if btts_recorded > 0 else 0
    
    # Confidence based on sample size and data quality
    base_confidence = min(total * 6, 95)
    data_quality = (btts_recorded / total) * 100 if total > 0 else 0
    confidence = int(min((base_confidence + data_quality) / 2 * 0.95, 99))
    
    return {
        'category': category,
        'win_rate': win_rate,
        'upset_rate': upset_rate,
        'btts_rate': btts_rate,
        'btts_data_count': btts_recorded,
        'confidence': confidence,
        'sample_size': total,
        'is_favorite': is_favorite,
        'odds_range': (min_odd, max_odd)
    }

def calculate_implied_probability(odds):
    """Calculate implied probability from odds (includes bookmaker margin)"""
    if not odds or odds <= 1:
        return 0
    return round((1 / odds) * 100, 1)

def is_value_bet(win_rate, implied_prob, odds, min_margin=5, min_confidence=50):
    """
    Detect value bets using multiple factors
    - Historical win% must exceed implied probability
    - Value margin must be significant (default 5%)
    - Higher odds get higher value threshold (larger underdogs need bigger edge)
    """
    if not win_rate or win_rate < 1:
        return False
    
    value_margin = win_rate - implied_prob
    
    # Adjust margin requirement based on odds (underdogs need bigger edge)
    if odds > 3.0:
        margin_threshold = 8  # Very heavy underdogs need 8% edge
    elif odds > 2.0:
        margin_threshold = 6
    else:
        margin_threshold = min_margin
    
    return value_margin >= margin_threshold

def generate_prediction(home_team, away_team, odds_1, odds_x, odds_2, source='Unknown'):
    """
    Generate comprehensive prediction with value bet detection and odds range analysis
    Outputs key metrics: win rates, upset rates, BTTS frequency, confidence, rationale
    """
    try:
        # Analyze each odds result
        analysis_1 = analyze_odds_range(odds_1, '1')
        analysis_x = analyze_odds_range(odds_x, 'X')
        analysis_2 = analyze_odds_range(odds_2, '2')
        
        # Calculate implied probabilities
        implied_1 = calculate_implied_probability(odds_1)
        implied_x = calculate_implied_probability(odds_x)
        implied_2 = calculate_implied_probability(odds_2)
        
        # Detect value bets with refined logic
        value_1 = is_value_bet(analysis_1['win_rate'], implied_1, odds_1)
        value_x = is_value_bet(analysis_x['win_rate'], implied_x, odds_x)
        value_2 = is_value_bet(analysis_2['win_rate'], implied_2, odds_2)
        
        # Find best overall prediction (highest win rate)
        predictions = [
            ('1', analysis_1['win_rate'], analysis_1),
            ('X', analysis_x['win_rate'], analysis_x),
            ('2', analysis_2['win_rate'], analysis_2)
        ]
        best_prediction, best_rate, best_analysis = max(predictions, key=lambda x: x[1])
        
        # Find best value bet (highest value margin)
        value_bets = []
        if value_1:
            value_bets.append({
                'prediction': '1',
                'odds': odds_1,
                'name': 'Home Win',
                'category': analysis_1['category'],
                'win_rate': analysis_1['win_rate'],
                'upset_rate': analysis_1['upset_rate'],
                'implied': implied_1,
                'value_margin': analysis_1['win_rate'] - implied_1,
                'confidence': analysis_1['confidence'],
                'sample_size': analysis_1['sample_size'],
                'btts_rate': analysis_1['btts_rate']
            })
        if value_x:
            value_bets.append({
                'prediction': 'X',
                'odds': odds_x,
                'name': 'Draw',
                'category': analysis_x['category'],
                'win_rate': analysis_x['win_rate'],
                'upset_rate': analysis_x['upset_rate'],
                'implied': implied_x,
                'value_margin': analysis_x['win_rate'] - implied_x,
                'confidence': analysis_x['confidence'],
                'sample_size': analysis_x['sample_size'],
                'btts_rate': analysis_x['btts_rate']
            })
        if value_2:
            value_bets.append({
                'prediction': '2',
                'odds': odds_2,
                'name': 'Away Win',
                'category': analysis_2['category'],
                'win_rate': analysis_2['win_rate'],
                'upset_rate': analysis_2['upset_rate'],
                'implied': implied_2,
                'value_margin': analysis_2['win_rate'] - implied_2,
                'confidence': analysis_2['confidence'],
                'sample_size': analysis_2['sample_size'],
                'btts_rate': analysis_2['btts_rate']
            })
        
        best_value = max(value_bets, key=lambda x: x['value_margin']) if value_bets else None
        
        # Generate rationale
        rationale_points = []
        if best_analysis['win_rate'] > 50:
            rationale_points.append(f"Strong: {best_analysis['win_rate']}% historical win rate")
        if best_analysis['win_rate'] > 35 and best_analysis['win_rate'] < 50:
            rationale_points.append(f"Moderate: {best_analysis['win_rate']}% historical win rate")
        if best_value:
            edge_pct = round(best_value['value_margin'], 1)
            rationale_points.append(f"💎 VALUE: {edge_pct}% edge vs bookmaker")
        if best_analysis['btts_rate'] > 55:
            rationale_points.append(f"BTTS likely: {best_analysis['btts_rate']}%")
        if best_analysis['upset_rate'] > 30:
            rationale_points.append(f"Upset risk: {best_analysis['upset_rate']}%")
        if best_analysis['sample_size'] < 5:
            rationale_points.append(f"⚠️ Limited data: {best_analysis['sample_size']} matches")
        
        return {
            'match': f"{home_team} vs {away_team}",
            'odds': {
                '1': odds_1,
                'X': odds_x,
                '2': odds_2
            },
            'analysis': {
                '1': analysis_1,
                'X': analysis_x,
                '2': analysis_2
            },
            'implied_probability': {
                '1': implied_1,
                'X': implied_x,
                '2': implied_2
            },
            'best_prediction': best_prediction,
            'best_win_rate': best_rate,
            'best_category': best_analysis['category'],
            'best_upset_rate': best_analysis['upset_rate'],
            'best_value_bet': best_value,
            'has_value_bets': len(value_bets) > 0,
            'all_value_bets': value_bets,
            'btts_rate': max(analysis_1['btts_rate'], analysis_x['btts_rate'], analysis_2['btts_rate']),
            'average_confidence': int((analysis_1['confidence'] + analysis_x['confidence'] + analysis_2['confidence']) / 3),
            'rationale': " | ".join(rationale_points) if rationale_points else "Based on historical odds analysis",
            'prediction_summary': {
                '1': {'win_rate': analysis_1['win_rate'], 'upset_rate': analysis_1['upset_rate'], 'btts': analysis_1['btts_rate']},
                'X': {'win_rate': analysis_x['win_rate'], 'upset_rate': analysis_x['upset_rate'], 'btts': analysis_x['btts_rate']},
                '2': {'win_rate': analysis_2['win_rate'], 'upset_rate': analysis_2['upset_rate'], 'btts': analysis_2['btts_rate']}
            }
        }
    except Exception as e:
        return {'error': str(e)}

def extract_odds_from_image(image_path):
    """
    Advanced OCR to extract all match details from screenshot
    Extracts: team names, odds, match time, source
    Returns: dict with extracted data
    
    NOTE: Requires Tesseract OCR engine installed on system
    Download from: https://github.com/UB-Mannheim/tesseract/wiki
    """
    if not HAS_PYTESSERACT:
        return {
            'success': False,
            'error': 'OCR engine not available',
            'note': 'Pytesseract not installed. Install with: pip install pytesseract',
            'solution': 'Install Tesseract OCR from https://github.com/UB-Mannheim/tesseract/wiki',
            'extracted_text': '',
            'teams': [],
            'odds': [],
        }
    
    try:
        import re
        from PIL import ImageEnhance, ImageFilter
        
        img = Image.open(image_path)
        
        # Enhanced image preprocessing for better OCR
        img = img.convert('RGB')
        
        # Increase contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0)
        
        # Convert to grayscale
        img = img.convert('L')
        
        # Apply threshold
        threshold = 150
        img = img.point(lambda p: p > threshold and 255)
        
        # Extract text with multiple PSM modes for better accuracy
        text_configs = [
            '--psm 6',  # Assume uniform block of text
            '--psm 4',  # Assume single column
            '--psm 3',  # Fully automatic page segmentation
        ]
        
        all_text = ""
        for config in text_configs:
            try:
                extracted = pytesseract.image_to_string(img, config=config)
                all_text += extracted + "\n"
            except:
                pass
        
        if not all_text.strip():
            all_text = pytesseract.image_to_string(img)
        
        # Enhanced pattern matching
        lines = all_text.split('\n')
        
        # Extract team names (look for "vs", "v", "-", or two capitalized words)
        teams = []
        team_patterns = [
            r'([A-Z][a-zA-Z\s]+?)\s+(?:vs|v|VS|V|-)\s+([A-Z][a-zA-Z\s]+)',
            r'([A-Z][a-zA-Z]+)\s+([A-Z][a-zA-Z]+)',  # Two capitalized words
        ]
        
        for line in lines:
            for pattern in team_patterns:
                match = re.search(pattern, line)
                if match:
                    home_team = match.group(1).strip()
                    away_team = match.group(2).strip()
                    if len(home_team) > 2 and len(away_team) > 2:
                        teams = [home_team, away_team]
                        break
            if teams:
                break
        
        # Extract odds (numbers between 1.01 and 99.99)
        numbers = re.findall(r'\b(\d+\.\d{2})\b|\b(\d{1,2}\.\d{1,2})\b', all_text)
        odds = []
        for match in numbers:
            for num in match:
                if num:
                    try:
                        odd_value = float(num)
                        if 1.01 <= odd_value <= 99.99:
                            odds.append(odd_value)
                    except:
                        pass
        
        # Remove duplicates while preserving order
        seen = set()
        unique_odds = []
        for odd in odds:
            if odd not in seen:
                seen.add(odd)
                unique_odds.append(odd)
        
        # Try to identify which odds are 1, X, 2
        # Typically they appear in order: Home, Draw, Away
        extracted_odds = {}
        if len(unique_odds) >= 3:
            extracted_odds = {
                'odds_1': unique_odds[0],
                'odds_x': unique_odds[1],
                'odds_2': unique_odds[2]
            }
        
        # Detect source (Betpawa, 1xbet, Bet365, etc)
        source = 'Unknown'
        source_keywords = {
            'betpawa': ['betpawa', 'bet pawa', 'betpawa.com'],
            '1xbet': ['1xbet', '1x bet', '1xbet.com'],
            'bet365': ['bet365', 'bet 365'],
            '22bet': ['22bet', '22 bet'],
            'sportybet': ['sportybet', 'sporty bet']
        }
        
        text_lower = all_text.lower()
        for source_name, keywords in source_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    source = source_name.capitalize() if source_name != '1xbet' else '1xbet'
                    break
            if source != 'Unknown':
                break
        
        # Extract match name from teams if found
        match_name = ""
        if len(teams) == 2:
            match_name = f"{teams[0]} vs {teams[1]}"
        
        return {
            'success': True,
            'extracted_text': all_text,
            'teams': teams,
            'home_team': teams[0] if len(teams) > 0 else '',
            'away_team': teams[1] if len(teams) > 1 else '',
            'match_name': match_name,
            'odds': unique_odds,
            'extracted_odds': extracted_odds,
            'source': source,
            'confidence': min(len(teams) * 30 + min(len(unique_odds), 3) * 20, 100)
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'teams': [],
            'odds': []
        }

def predict_next_odds(history_records, home_team=None, away_team=None):
    """
    Advanced prediction using historical trends and win percentages
    Compares past results to predict upcoming fixtures
    """
    if len(history_records) < 2:
        return None
    
    try:
        # Get completed matches with results
        completed_matches = [r for r in history_records if r.is_completed and r.actual_result]
        
        prediction = {}
        
        # ADVANCED: Calculate win percentages from historical results
        if len(completed_matches) >= 3:
            total_completed = len(completed_matches)
            wins_1 = len([r for r in completed_matches if r.actual_result == '1'])
            wins_x = len([r for r in completed_matches if r.actual_result == 'X'])
            wins_2 = len([r for r in completed_matches if r.actual_result == '2'])
            
            prediction['win_rate_1'] = round((wins_1 / total_completed) * 100, 1)
            prediction['win_rate_x'] = round((wins_x / total_completed) * 100, 1)
            prediction['win_rate_2'] = round((wins_2 / total_completed) * 100, 1)
            
            # Calculate odds value analysis (comparing odds vs actual outcomes)
            odds_value_analysis = {'1': [], 'X': [], '2': []}
            for match in completed_matches:
                if match.odds_1 and match.actual_result:
                    # Calculate implied probability vs actual outcome
                    implied_prob_1 = (1 / match.odds_1) * 100 if match.odds_1 else 0
                    implied_prob_x = (1 / match.odds_x) * 100 if match.odds_x else 0
                    implied_prob_2 = (1 / match.odds_2) * 100 if match.odds_2 else 0
                    
                    odds_value_analysis[match.actual_result].append({
                        'odds_1': match.odds_1,
                        'odds_x': match.odds_x,
                        'odds_2': match.odds_2,
                        'implied_1': implied_prob_1,
                        'implied_x': implied_prob_x,
                        'implied_2': implied_prob_2
                    })
            
            # Find patterns: when underdogs win, when favorites win, etc.
            underdog_wins = 0
            favorite_wins = 0
            for match in completed_matches:
                if match.odds_1 and match.odds_x and match.odds_2:
                    min_odd = min(match.odds_1, match.odds_x, match.odds_2)
                    if min_odd == match.odds_1 and match.actual_result == '1':
                        favorite_wins += 1
                    elif match.actual_result == '1' and match.odds_1 > min(match.odds_x, match.odds_2):
                        underdog_wins += 1
            
            prediction['favorite_win_rate'] = round((favorite_wins / total_completed) * 100, 1)
            prediction['underdog_win_rate'] = round((underdog_wins / total_completed) * 100, 1)
            
            # Determine recommended bet based on win rates
            win_rates = {
                '1': prediction['win_rate_1'],
                'X': prediction['win_rate_x'],
                '2': prediction['win_rate_2']
            }
            prediction['recommended_bet'] = max(win_rates, key=win_rates.get)
            prediction['recommended_bet_rate'] = win_rates[prediction['recommended_bet']]
            
            # ENHANCED: Team-specific head-to-head analysis
            if home_team and away_team:
                # Exact match: both teams playing each other
                h2h_matches = [r for r in completed_matches 
                              if r.home_team and r.away_team and
                                 home_team.lower() in r.home_team.lower() and 
                                 away_team.lower() in r.away_team.lower()]
                
                if len(h2h_matches) >= 1:
                    h2h_wins_1 = len([r for r in h2h_matches if r.actual_result == '1'])
                    h2h_wins_x = len([r for r in h2h_matches if r.actual_result == 'X'])
                    h2h_wins_2 = len([r for r in h2h_matches if r.actual_result == '2'])
                    total_h2h = len(h2h_matches)
                    
                    prediction['head_to_head'] = {
                        'matches_found': total_h2h,
                        'win_rate_1': round((h2h_wins_1 / total_h2h) * 100, 1),
                        'win_rate_x': round((h2h_wins_x / total_h2h) * 100, 1),
                        'win_rate_2': round((h2h_wins_2 / total_h2h) * 100, 1),
                        'recommended': max([('1', h2h_wins_1), ('X', h2h_wins_x), ('2', h2h_wins_2)], key=lambda x: x[1])[0]
                    }
                
                # Individual team performance
                team_matches = [r for r in completed_matches 
                               if (r.home_team and (home_team.lower() in r.home_team.lower() or away_team.lower() in r.home_team.lower())) or 
                                  (r.away_team and (home_team.lower() in r.away_team.lower() or away_team.lower() in r.away_team.lower()))]
                
                if len(team_matches) >= 2:
                    team_wins_1 = len([r for r in team_matches if r.actual_result == '1'])
                    team_wins_x = len([r for r in team_matches if r.actual_result == 'X'])
                    team_wins_2 = len([r for r in team_matches if r.actual_result == '2'])
                    total_team = len(team_matches)
                    
                    prediction['team_specific'] = {
                        'matches_found': total_team,
                        'win_rate_1': round((team_wins_1 / total_team) * 100, 1),
                        'win_rate_x': round((team_wins_x / total_team) * 100, 1),
                        'win_rate_2': round((team_wins_2 / total_team) * 100, 1)
                    }
            
            # Recent form analysis (last 5 matches)
            recent_matches = completed_matches[:min(5, len(completed_matches))]
            if len(recent_matches) >= 3:
                recent_1 = len([r for r in recent_matches if r.actual_result == '1'])
                recent_x = len([r for r in recent_matches if r.actual_result == 'X'])
                recent_2 = len([r for r in recent_matches if r.actual_result == '2'])
                total_recent = len(recent_matches)
                
                prediction['recent_form'] = {
                    'matches': total_recent,
                    'win_rate_1': round((recent_1 / total_recent) * 100, 1),
                    'win_rate_x': round((recent_x / total_recent) * 100, 1),
                    'win_rate_2': round((recent_2 / total_recent) * 100, 1),
                    'trend': 'home' if recent_1 > max(recent_x, recent_2) else ('draw' if recent_x > recent_2 else 'away')
                }
        
        # Calculate odds trends (moving average)
        odds_1_values = [r.odds_1 for r in history_records if r.odds_1]
        odds_x_values = [r.odds_x for r in history_records if r.odds_x]
        odds_2_values = [r.odds_2 for r in history_records if r.odds_2]
        
        if len(odds_1_values) >= 2:
            trend_1 = np.mean(odds_1_values[-3:]) if len(odds_1_values) >= 3 else odds_1_values[-1]
            prediction['odds_1_prediction'] = round(trend_1, 2)
            prediction['odds_1_trend'] = 'UP' if trend_1 > odds_1_values[-1] else 'DOWN'
        
        if len(odds_x_values) >= 2:
            trend_x = np.mean(odds_x_values[-3:]) if len(odds_x_values) >= 3 else odds_x_values[-1]
            prediction['odds_x_prediction'] = round(trend_x, 2)
            prediction['odds_x_trend'] = 'UP' if trend_x > odds_x_values[-1] else 'DOWN'
        
        if len(odds_2_values) >= 2:
            trend_2 = np.mean(odds_2_values[-3:]) if len(odds_2_values) >= 3 else odds_2_values[-1]
            prediction['odds_2_prediction'] = round(trend_2, 2)
            prediction['odds_2_trend'] = 'UP' if trend_2 > odds_2_values[-1] else 'DOWN'
        
        # Enhanced confidence calculation
        confidence = 0
        confidence += min(len(completed_matches) * 10, 50)  # Up to 50 points for completed matches
        confidence += min(len(history_records) * 3, 30)  # Up to 30 points for total history
        if prediction.get('head_to_head'):
            confidence += 20  # Bonus for head-to-head data
        
        prediction['confidence'] = min(confidence, 95)
        prediction['total_completed_matches'] = len(completed_matches)
        prediction['total_analyzed_matches'] = len(history_records)
        
        return prediction
    except Exception as e:
        return {'error': str(e)}
        
        # Calculate odds trends (moving average)
        odds_1_values = [r.odds_1 for r in history_records if r.odds_1]
        odds_x_values = [r.odds_x for r in history_records if r.odds_x]
        odds_2_values = [r.odds_2 for r in history_records if r.odds_2]
        
        if len(odds_1_values) >= 2:
            trend_1 = np.mean(odds_1_values[-3:]) if len(odds_1_values) >= 3 else odds_1_values[-1]
            prediction['odds_1_prediction'] = round(trend_1, 2)
            prediction['odds_1_trend'] = 'UP' if trend_1 > odds_1_values[-1] else 'DOWN'
        
        if len(odds_x_values) >= 2:
            trend_x = np.mean(odds_x_values[-3:]) if len(odds_x_values) >= 3 else odds_x_values[-1]
            prediction['odds_x_prediction'] = round(trend_x, 2)
            prediction['odds_x_trend'] = 'UP' if trend_x > odds_x_values[-1] else 'DOWN'
        
        if len(odds_2_values) >= 2:
            trend_2 = np.mean(odds_2_values[-3:]) if len(odds_2_values) >= 3 else odds_2_values[-1]
            prediction['odds_2_prediction'] = round(trend_2, 2)
            prediction['odds_2_trend'] = 'UP' if trend_2 > odds_2_values[-1] else 'DOWN'
        
        prediction['confidence'] = min(len(completed_matches) * 15 + len(history_records) * 5, 95)
        prediction['total_completed_matches'] = len(completed_matches)
        prediction['total_analyzed_matches'] = len(history_records)
        
        return prediction
    except Exception as e:
        return {'error': str(e)}

# Routes
@app.route('/')
def index():
    """
    Main landing page showing past results and upcoming match predictions
    """
    try:
        # Get past completed matches (limited to 10 most recent)
        past_matches = OddsRecord.query.filter_by(
            is_completed=True
        ).order_by(OddsRecord.uploaded_at.desc()).limit(10).all()
        
        # Get upcoming matches (not completed)
        upcoming_matches = OddsRecord.query.filter_by(
            is_completed=False
        ).order_by(OddsRecord.uploaded_at.desc()).limit(10).all()
        
        # Generate predictions for upcoming matches based on historical odds trends
        predictions = []
        all_completed = OddsRecord.query.filter_by(is_completed=True).order_by(
            OddsRecord.uploaded_at.desc()
        ).limit(100).all()
        
        for match in upcoming_matches:
            # Analyze each outcome based on historical data
            analysis_1 = analyze_odds_range(match.odds_1, '1') if match.odds_1 else None
            analysis_x = analyze_odds_range(match.odds_x, 'X') if match.odds_x else None
            analysis_2 = analyze_odds_range(match.odds_2, '2') if match.odds_2 else None
            
            # Determine best prediction
            best_bet = None
            best_confidence = 0
            
            if analysis_1 and analysis_1['win_rate'] > best_confidence:
                best_bet = '1'
                best_confidence = analysis_1['win_rate']
            if analysis_x and analysis_x['win_rate'] > best_confidence:
                best_bet = 'X'
                best_confidence = analysis_x['win_rate']
            if analysis_2 and analysis_2['win_rate'] > best_confidence:
                best_bet = '2'
                best_confidence = analysis_2['win_rate']
            
            predictions.append({
                'match': match,
                'prediction': best_bet,
                'confidence': round(best_confidence, 1) if best_confidence else 0,
                'analysis_1': analysis_1,
                'analysis_x': analysis_x,
                'analysis_2': analysis_2
            })
        
        return render_template('home.html', 
                             past_matches=past_matches,
                             upcoming_matches=predictions,
                             total_past=len(past_matches),
                             total_upcoming=len(upcoming_matches))
    except Exception as e:
        app.logger.error(f"Error in index route: {str(e)}")
        return render_template('home.html', 
                             past_matches=[],
                             upcoming_matches=[],
                             total_past=0,
                             total_upcoming=0)

@app.route('/admin')
def admin():
    """
    Admin page for uploading and managing match data
    """
    return render_template('index.html')

@app.route('/init-data')
def manual_init_data():
    """
    Manually trigger database initialization (useful if auto-init didn't run)
    """
    try:
        count_before = OddsRecord.query.count()
        init_sample_data()
        count_after = OddsRecord.query.count()
        added = count_after - count_before
        
        return jsonify({
            'success': True,
            'message': f'Database initialized successfully',
            'matches_before': count_before,
            'matches_after': count_after,
            'matches_added': added
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/reset-database')
def reset_database():
    """
    FORCE RESET: Delete all data and reinitialize with fresh upcoming matches
    Use this to fix old/incorrect data on live site
    """
    try:
        # Delete ALL existing data
        count_before = OddsRecord.query.count()
        OddsRecord.query.delete()
        db.session.commit()
        
        # Reinitialize with fresh data
        init_sample_data()
        
        count_after = OddsRecord.query.count()
        past = OddsRecord.query.filter_by(is_completed=True).count()
        upcoming = OddsRecord.query.filter_by(is_completed=False).count()
        
        return jsonify({
            'success': True,
            'message': 'Database reset successfully with fresh data',
            'old_matches_deleted': count_before,
            'new_matches_added': count_after,
            'past_matches': past,
            'upcoming_matches': upcoming
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/refresh-fixtures')
def refresh_live_fixtures():
    """
    Refresh upcoming fixtures from live web sources (tomorrow's matches)
    """
    try:
        from fetch_live_fixtures import update_live_fixtures
        
        count_before = OddsRecord.query.filter_by(is_completed=False).count()
        update_live_fixtures()
        count_after = OddsRecord.query.filter_by(is_completed=False).count()
        added = count_after - count_before
        
        return jsonify({
            'success': True,
            'message': 'Live fixtures refreshed from web sources',
            'upcoming_matches_before': count_before,
            'upcoming_matches_after': count_after,
            'new_matches': added
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Upload screenshot(s) and auto-extract all details using OCR
    Supports single and multiple file uploads
    """
    if 'file' not in request.files:
        app.logger.warning('Upload request with no file provided')
        return jsonify({'error': 'No file provided'}), 400
    
    files = request.files.getlist('file')
    if not files or files[0].filename == '':
        app.logger.warning('Upload request with no file selected')
        return jsonify({'error': 'No file selected'}), 400
    
    app.logger.info(f'Upload initiated: {len(files)} file(s)')
    results = []
    errors = []
    
    for file in files:
        if not allowed_file(file.filename):
            warning_msg = f'{file.filename}: Invalid file type'
            app.logger.warning(warning_msg)
            errors.append(warning_msg)
            continue
        
        try:
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # AUTO-EXTRACT ALL DETAILS from image using advanced OCR
            extraction = extract_odds_from_image(filepath)
            
            # Use extracted data if available, otherwise use form data as fallback
            match_name = extraction.get('match_name') or request.form.get('match_name', 'Unknown Match')
            home_team = extraction.get('home_team') or request.form.get('home_team', '')
            away_team = extraction.get('away_team') or request.form.get('away_team', '')
            source = extraction.get('source', 'Unknown')
            if source == 'Unknown':
                source = request.form.get('source', 'Unknown')
            
            # Get odds from extraction or form
            extracted_odds = extraction.get('extracted_odds', {})
            odds_1 = extracted_odds.get('odds_1') or float(request.form.get('odds_1', 0) or 0)
            odds_x = extracted_odds.get('odds_x') or float(request.form.get('odds_x', 0) or 0)
            odds_2 = extracted_odds.get('odds_2') or float(request.form.get('odds_2', 0) or 0)
            
            # Override with form data if provided
            if request.form.get('odds_1'):
                odds_1 = float(request.form.get('odds_1'))
            if request.form.get('odds_x'):
                odds_x = float(request.form.get('odds_x'))
            if request.form.get('odds_2'):
                odds_2 = float(request.form.get('odds_2'))
            
            notes = request.form.get('notes', '')
            
            # Save to database
            record = OddsRecord(
                match_name=match_name,
                home_team=home_team,
                away_team=away_team,
                odds_1=odds_1 if odds_1 > 0 else None,
                odds_x=odds_x if odds_x > 0 else None,
                odds_2=odds_2 if odds_2 > 0 else None,
                source=source,
                image_path=filename,
                notes=notes
            )
            db.session.add(record)
            db.session.commit()
            
            # Auto-generate prediction based on historical data
            history = OddsRecord.query.filter_by(source=source).order_by(
                OddsRecord.uploaded_at.desc()
            ).limit(30).all()
            
            prediction = predict_next_odds(history, home_team, away_team)
            
            results.append({
                'record_id': record.id,
                'filename': file.filename,
                'match_name': match_name,
                'teams': f"{home_team} vs {away_team}" if home_team and away_team else match_name,
                'extracted_data': {
                    'home_team': home_team,
                    'away_team': away_team,
                    'odds_1': odds_1,
                    'odds_x': odds_x,
                    'odds_2': odds_2,
                    'source': source,
                    'confidence': extraction.get('confidence', 0)
                },
                'prediction': prediction
            })
        
        except Exception as e:
            app.logger.error(f'Error processing {file.filename}: {str(e)}', exc_info=True)
            errors.append(f'{file.filename}: {str(e)}')
            try:
                db.session.rollback()
            except:
                pass
            continue
    
    if not results:
        return jsonify({
            'success': False,
            'error': 'Failed to process any files',
            'errors': errors
        }), 500
    
    return jsonify({
        'success': True,
        'message': f'Successfully processed {len(results)} file(s)',
        'count': len(results),
        'results': results,
        'errors': errors if errors else None
    })

@app.route('/history')
def get_history():
    """
    Get all odds records
    """
    try:
        limit = request.args.get('limit', 50, type=int)
        records = OddsRecord.query.order_by(OddsRecord.uploaded_at.desc()).limit(limit).all()
        
        data = []
        for r in records:
            data.append({
                'id': r.id,
                'match_name': r.match_name,
                'home_team': r.home_team,
                'away_team': r.away_team,
                'odds_1': r.odds_1,
                'odds_x': r.odds_x,
                'odds_2': r.odds_2,
                'source': r.source,
                'uploaded_at': r.uploaded_at.strftime('%Y-%m-%d %H:%M:%S'),
                'is_completed': r.is_completed,
                'actual_result': r.actual_result,
                'btts': r.btts,
                'goals_for': r.goals_for,
                'notes': r.notes
            })
        
        return jsonify({'records': data, 'total': len(data)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict/<int:match_id>')
def get_prediction(match_id):
    """
    Get prediction for a specific match based on historical odds
    """
    try:
        match = OddsRecord.query.get(match_id)
        if not match:
            return jsonify({'error': 'Match not found'}), 404
        
        # Get history for similar matches
        history = OddsRecord.query.filter_by(source=match.source).order_by(
            OddsRecord.uploaded_at.desc()
        ).limit(30).all()
        
        prediction = predict_next_odds(history, match.home_team, match.away_team)
        
        return jsonify({
            'match_id': match_id,
            'match_name': match.match_name,
            'current_odds': {
                'odds_1': match.odds_1,
                'odds_x': match.odds_x,
                'odds_2': match.odds_2
            },
            'prediction': prediction,
            'history_count': len(history)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stats')
def get_stats():
    """
    Get general statistics
    """
    try:
        total_records = OddsRecord.query.count()
        betpawa_count = OddsRecord.query.filter_by(source='Betpawa').count()
        one_xbet_count = OddsRecord.query.filter_by(source='1xbet').count()
        
        avg_odds_1 = db.session.query(db.func.avg(OddsRecord.odds_1)).scalar() or 0
        avg_odds_x = db.session.query(db.func.avg(OddsRecord.odds_x)).scalar() or 0
        avg_odds_2 = db.session.query(db.func.avg(OddsRecord.odds_2)).scalar() or 0
        
        completed_matches_count = OddsRecord.query.filter_by(is_completed=True).count()
        pending_matches_count = OddsRecord.query.filter_by(is_completed=False).count()
        
        # Calculate win rate statistics if we have completed matches
        completed = OddsRecord.query.filter_by(is_completed=True).all()
        
        response_data = {
            'total_records': total_records,
            'betpawa_count': betpawa_count,
            'one_xbet_count': one_xbet_count,
            'completed_matches': completed_matches_count,
            'pending_matches': pending_matches_count,
            'average_odds': {
                'odds_1': round(avg_odds_1, 2),
                'odds_x': round(avg_odds_x, 2),
                'odds_2': round(avg_odds_2, 2)
            }
        }
        
        if completed and len(completed) > 0:
            total_completed = len(completed)
            wins_1 = len([r for r in completed if r.actual_result == '1'])
            wins_x = len([r for r in completed if r.actual_result == 'X'])
            wins_2 = len([r for r in completed if r.actual_result == '2'])
            
            response_data['win_rates'] = {
                'home_wins': round((wins_1 / total_completed) * 100, 1),
                'draws': round((wins_x / total_completed) * 100, 1),
                'away_wins': round((wins_2 / total_completed) * 100, 1),
                'total_analyzed': total_completed
            }
        
        return jsonify(response_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/update_result/<int:record_id>', methods=['POST'])
def update_result(record_id):
    """
    Update match result after game is completed
    """
    try:
        record = OddsRecord.query.get(record_id)
        if not record:
            return jsonify({'error': 'Record not found'}), 404
        
        result = request.json.get('result')  # '1', 'X', or '2'
        if result not in ['1', 'X', '2']:
            return jsonify({'error': 'Invalid result. Must be 1, X, or 2'}), 400
        
        record.actual_result = result
        record.is_completed = True
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Match result updated successfully',
            'record_id': record_id,
            'result': result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    """
    Delete a record
    """
    try:
        record = OddsRecord.query.get(record_id)
        if not record:
            return jsonify({'error': 'Record not found'}), 404
        
        if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], record.image_path)):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], record.image_path))
        
        db.session.delete(record)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Record deleted'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/image/<filename>')
def get_image(filename):
    """
    Serve uploaded images
    """
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/odds-analysis', methods=['POST'])
def analyze_odds():
    """
    Advanced odds analysis with value bet detection
    Input: odds_1, odds_x, odds_2, home_team, away_team
    Output: Win rates, BTTS rates, value bets, predictions
    """
    try:
        data = request.json
        odds_1 = float(data.get('odds_1', 0))
        odds_x = float(data.get('odds_x', 0))
        odds_2 = float(data.get('odds_2', 0))
        home_team = data.get('home_team', 'Unknown')
        away_team = data.get('away_team', 'Unknown')
        source = data.get('source', 'Unknown')
        
        # Generate comprehensive prediction
        prediction = generate_prediction(home_team, away_team, odds_1, odds_x, odds_2, source)
        
        if 'error' in prediction:
            return jsonify(prediction), 400
        
        return jsonify(prediction)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/update-btts/<int:record_id>', methods=['POST'])
def update_btts(record_id):
    """
    Update BTTS (Both Teams To Score) result for a match
    Input: btts ('Y' or 'N'), goals_for (optional: total goals)
    """
    try:
        record = OddsRecord.query.get(record_id)
        if not record:
            return jsonify({'error': 'Record not found'}), 404
        
        btts = request.json.get('btts')  # 'Y' or 'N'
        goals_for = request.json.get('goals_for')  # Total goals
        
        if btts and btts in ['Y', 'N']:
            record.btts = btts
        
        if goals_for:
            record.goals_for = int(goals_for)
            # Auto-detect BTTS from goals if not set
            if not record.btts and goals_for > 0:
                record.btts = 'Y' if goals_for >= 2 else 'N'
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'BTTS updated successfully',
            'btts': record.btts,
            'goals': record.goals_for
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/value-bets')
def get_value_bets():
    """
    Get list of value bets detected from historical data
    Value bets: historical win% > implied probability
    """
    try:
        source = request.args.get('source', None)
        
        # Get all completed matches
        if source:
            matches = OddsRecord.query.filter_by(source=source, is_completed=True).all()
        else:
            matches = OddsRecord.query.filter_by(is_completed=True).all()
        
        value_bets = []
        
        for match in matches:
            if not match.odds_1 or not match.actual_result:
                continue
            
            # Calculate win rates for each outcome
            analysis_1 = analyze_odds_range(match.odds_1, '1')
            analysis_x = analyze_odds_range(match.odds_x, 'X') if match.odds_x else {}
            analysis_2 = analyze_odds_range(match.odds_2, '2') if match.odds_2 else {}
            
            # Check for value
            implied_1 = calculate_implied_probability(match.odds_1)
            implied_x = calculate_implied_probability(match.odds_x) if match.odds_x else 0
            implied_2 = calculate_implied_probability(match.odds_2) if match.odds_2 else 0
            
            # Detect value bets
            if analysis_1.get('win_rate', 0) > implied_1 + 5:
                value_bets.append({
                    'match_name': match.match_name,
                    'teams': f"{match.home_team} vs {match.away_team}",
                    'bet_type': 'Home Win',
                    'odds': match.odds_1,
                    'historical_win_rate': analysis_1.get('win_rate', 0),
                    'implied_probability': implied_1,
                    'value_edge': round(analysis_1.get('win_rate', 0) - implied_1, 1),
                    'confidence': analysis_1.get('confidence', 0),
                    'sample_size': analysis_1.get('sample_size', 0)
                })
            
            if match.odds_x and analysis_x.get('win_rate', 0) > implied_x + 5:
                value_bets.append({
                    'match_name': match.match_name,
                    'teams': f"{match.home_team} vs {match.away_team}",
                    'bet_type': 'Draw',
                    'odds': match.odds_x,
                    'historical_win_rate': analysis_x.get('win_rate', 0),
                    'implied_probability': implied_x,
                    'value_edge': round(analysis_x.get('win_rate', 0) - implied_x, 1),
                    'confidence': analysis_x.get('confidence', 0),
                    'sample_size': analysis_x.get('sample_size', 0)
                })
            
            if match.odds_2 and analysis_2.get('win_rate', 0) > implied_2 + 5:
                value_bets.append({
                    'match_name': match.match_name,
                    'teams': f"{match.home_team} vs {match.away_team}",
                    'bet_type': 'Away Win',
                    'odds': match.odds_2,
                    'historical_win_rate': analysis_2.get('win_rate', 0),
                    'implied_probability': implied_2,
                    'value_edge': round(analysis_2.get('win_rate', 0) - implied_2, 1),
                    'confidence': analysis_2.get('confidence', 0),
                    'sample_size': analysis_2.get('sample_size', 0)
                })
        
        # Sort by value edge (highest first)
        value_bets.sort(key=lambda x: x['value_edge'], reverse=True)
        
        return jsonify({
            'value_bets': value_bets,
            'total_found': len(value_bets),
            'message': f'Found {len(value_bets)} value betting opportunities'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/odds-report')
def generate_odds_report():
    """
    Generate comprehensive odds analysis report
    Table format: Match | Odds | Historical Win % | BTTS % | Prediction | Rationale
    """
    try:
        source = request.args.get('source', None)
        limit = request.args.get('limit', 20, type=int)
        
        # Get recent records
        if source:
            records = OddsRecord.query.filter_by(source=source).order_by(
                OddsRecord.uploaded_at.desc()
            ).limit(limit).all()
        else:
            records = OddsRecord.query.order_by(
                OddsRecord.uploaded_at.desc()
            ).limit(limit).all()
        
        report_data = []
        
        for record in records:
            if not record.odds_1 or not record.odds_x or not record.odds_2:
                continue
            
            # Generate prediction with value detection
            pred = generate_prediction(
                record.home_team, 
                record.away_team, 
                record.odds_1, 
                record.odds_x, 
                record.odds_2, 
                record.source
            )
            
            # Extract analysis for best prediction
            best_analysis = pred['analysis'].get(pred['best_prediction'], {})
            
            # Determine prediction display
            pred_display = {
                '1': '🏠 Home',
                'X': '🤝 Draw',
                '2': '✈️ Away'
            }.get(pred['best_prediction'], 'Unknown')
            
            # Get odds for best prediction
            best_odds = {
                '1': record.odds_1,
                'X': record.odds_x,
                '2': record.odds_2
            }.get(pred['best_prediction'], 0)
            
            # Build rationale using new metrics
            rationale_parts = []
            win_rate = best_analysis.get('win_rate', 0)
            upset_rate = best_analysis.get('upset_rate', 0)
            btts_rate = best_analysis.get('btts_rate', 0)
            confidence = best_analysis.get('confidence', 0)
            sample_size = best_analysis.get('sample_size', 0)
            is_favorite = best_analysis.get('is_favorite', False)
            
            if win_rate > 60:
                rationale_parts.append(f"💪 Very Strong: {win_rate}% win rate ({sample_size} matches)")
            elif win_rate > 50:
                rationale_parts.append(f"📈 Strong: {win_rate}% win rate ({sample_size} matches)")
            elif win_rate > 40:
                rationale_parts.append(f"⚖️ Balanced: {win_rate}% win rate ({sample_size} matches)")
            
            if is_favorite and upset_rate > 25:
                rationale_parts.append(f"⚠️ Favorite upset: {upset_rate}% lose rate")
            elif not is_favorite and upset_rate > 40:
                rationale_parts.append(f"🎯 Underdog ready: {upset_rate}% win rate")
            
            if pred.get('best_value_bet'):
                value_margin = round(pred['best_value_bet']['value_margin'], 1)
                rationale_parts.append(f"💎 VALUE: {value_margin}% edge vs bookmaker")
            
            if btts_rate > 65:
                rationale_parts.append(f"⚽ BTTS High: {btts_rate}%")
            elif btts_rate > 50:
                rationale_parts.append(f"⚽ BTTS Likely: {btts_rate}%")
            
            if confidence >= 85:
                rationale_parts.append(f"✅ High confidence: {confidence}%")
            elif sample_size < 3:
                rationale_parts.append(f"⚠️ Low data: {sample_size} matches only")
            
            rationale = " | ".join(rationale_parts) if rationale_parts else "Moderate historical analysis"
            
            # Status indicator
            status = ""
            if record.is_completed:
                status = "✅ COMPLETE" if record.actual_result else "⏳ PENDING"
            else:
                status = "⏳ PENDING"
            
            report_data.append({
                'match_id': record.id,
                'match': f"{record.home_team} vs {record.away_team}",
                'status': status,
                'odds_1': round(record.odds_1, 2) if record.odds_1 else None,
                'odds_x': round(record.odds_x, 2) if record.odds_x else None,
                'odds_2': round(record.odds_2, 2) if record.odds_2 else None,
                'odds_range': best_analysis.get('category', 'Unknown'),
                'best_prediction': pred_display,
                'best_odds': round(best_odds, 2) if best_odds else 0,
                'historical_win_rate': best_analysis.get('win_rate', 0),
                'upset_rate': best_analysis.get('upset_rate', 0),
                'btts_rate': best_analysis.get('btts_rate', 0),
                'confidence': best_analysis.get('confidence', 0),
                'sample_size': best_analysis.get('sample_size', 0),
                'is_favorite': best_analysis.get('is_favorite', False),
                'rationale': rationale,
                'value_bet': pred.get('best_value_bet'),
                'is_value_opportunity': pred.get('has_value_bets', False),
                'uploaded_at': record.uploaded_at.strftime('%Y-%m-%d %H:%M:%S'),
                'source': record.source,
                'all_value_bets': pred.get('all_value_bets', [])
            })
        
        return jsonify({
            'report': report_data,
            'total_matches': len(report_data),
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def parse_odds_from_prompt(prompt):
    """
    Parse odds from natural language prompts
    Examples:
    - "Calculate win probability for odds 1.8 vs 4.0"
    - "Analyze 1.5-2.5-6.0"
    - "1.80 vs 4.0 underdog"
    Returns: (odds_1, odds_x, odds_2) or None
    """
    import re
    
    # Find all decimal numbers in the prompt
    numbers = re.findall(r'\d+\.?\d*', prompt)
    numbers = [float(n) for n in numbers if 1.0 <= float(n) <= 99.99]
    
    if len(numbers) >= 2:
        # If we have at least 2 odds, use them
        odds_1 = numbers[0]
        odds_2 = numbers[1]
        # For draw, use average or extract if 3 numbers provided
        odds_x = numbers[2] if len(numbers) >= 3 else round((odds_1 + odds_2) / 2, 2)
        return (odds_1, odds_x, odds_2)
    
    return None

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """
    API endpoint to predict odds outcome from text prompt
    Request: POST /api/predict
    Body: {"prompt": "Calculate win probability for odds 1.8 vs 4.0"}
    
    Returns: {
        "success": true,
        "match": "Analysis",
        "odds_1": 1.8,
        "odds_x": 2.9,
        "odds_2": 4.0,
        "analysis_1": {win_rate, upset_rate, btts_rate, confidence, sample_size},
        "analysis_x": {...},
        "analysis_2": {...},
        "best_prediction": "1",
        "best_win_rate": 62.5,
        "prediction_summary": {...},
        "rationale": "Smart explanation"
    }
    """
    try:
        data = request.get_json()
        if not data:
            app.logger.warning('API predict called with no JSON body')
            return jsonify({'error': 'No JSON body provided'}), 400
        
        prompt = data.get('prompt', '').strip()
        if not prompt:
            app.logger.warning('API predict called with empty prompt')
            return jsonify({'error': 'No prompt provided'}), 400
        
        # Validate prompt length
        if len(prompt) > MAX_PROMPT_LENGTH:
            app.logger.warning(f'API predict called with prompt too long: {len(prompt)} chars')
            return jsonify({
                'error': f'Prompt too long. Maximum {MAX_PROMPT_LENGTH} characters allowed.',
                'received': len(prompt)
            }), 413
        
        # Parse odds from prompt
        odds_tuple = parse_odds_from_prompt(prompt)
        if not odds_tuple:
            app.logger.info(f'Could not parse odds from prompt: {prompt[:100]}')
            return jsonify({
                'error': 'Could not parse odds from prompt. Try: "1.8 vs 4.0" or "1.5-2.5-6.0"',
                'prompt': prompt[:100]
            }), 400
        
        odds_1, odds_x, odds_2 = odds_tuple
        
        # Run analysis for each odds type
        analysis_1 = analyze_odds_range(odds_1, '1')
        analysis_x = analyze_odds_range(odds_x, 'X')
        analysis_2 = analyze_odds_range(odds_2, '2')
        
        # Calculate implied probabilities
        implied_1 = calculate_implied_probability(odds_1)
        implied_x = calculate_implied_probability(odds_x)
        implied_2 = calculate_implied_probability(odds_2)
        
        # Determine best prediction
        predictions = [
            ('1', analysis_1['win_rate'], analysis_1),
            ('X', analysis_x['win_rate'], analysis_x),
            ('2', analysis_2['win_rate'], analysis_2)
        ]
        best_prediction, best_rate, best_analysis = max(predictions, key=lambda x: x[1])
        
        # Generate smart rationale
        rationale_parts = []
        if best_rate > 60:
            rationale_parts.append(f"Strong: {best_rate}% win rate ({best_analysis['sample_size']} matches)")
        elif best_rate > 50:
            rationale_parts.append(f"Moderate: {best_rate}% win rate ({best_analysis['sample_size']} matches)")
        elif best_rate > 40:
            rationale_parts.append(f"Balanced: {best_rate}% win rate ({best_analysis['sample_size']} matches)")
        
        if best_analysis['upset_rate'] > 30:
            if best_analysis['is_favorite']:
                rationale_parts.append(f"Favorite risk: {best_analysis['upset_rate']}%")
            else:
                rationale_parts.append(f"Underdog opportunity: {best_analysis['upset_rate']}%")
        
        if best_analysis['btts_rate'] > 55:
            rationale_parts.append(f"BTTS High: {best_analysis['btts_rate']}%")
        
        if best_analysis['confidence'] >= 80:
            rationale_parts.append(f"High confidence: {best_analysis['confidence']}%")
        elif best_analysis['sample_size'] < 3:
            rationale_parts.append(f"Low data: {best_analysis['sample_size']} matches")
        
        rationale = " | ".join(rationale_parts) if rationale_parts else "Awaiting historical data"
        
        return jsonify({
            'success': True,
            'match': 'Quick Analysis',
            'odds_1': round(odds_1, 2),
            'odds_x': round(odds_x, 2),
            'odds_2': round(odds_2, 2),
            'implied_probability': {
                '1': implied_1,
                'X': implied_x,
                '2': implied_2
            },
            'analysis_1': {
                'category': analysis_1['category'],
                'win_rate': analysis_1['win_rate'],
                'upset_rate': analysis_1['upset_rate'],
                'btts_rate': analysis_1['btts_rate'],
                'confidence': analysis_1['confidence'],
                'sample_size': analysis_1['sample_size'],
                'is_favorite': analysis_1['is_favorite']
            },
            'analysis_x': {
                'category': analysis_x['category'],
                'win_rate': analysis_x['win_rate'],
                'upset_rate': analysis_x['upset_rate'],
                'btts_rate': analysis_x['btts_rate'],
                'confidence': analysis_x['confidence'],
                'sample_size': analysis_x['sample_size']
            },
            'analysis_2': {
                'category': analysis_2['category'],
                'win_rate': analysis_2['win_rate'],
                'upset_rate': analysis_2['upset_rate'],
                'btts_rate': analysis_2['btts_rate'],
                'confidence': analysis_2['confidence'],
                'sample_size': analysis_2['sample_size'],
                'is_favorite': analysis_2['is_favorite']
            },
            'best_prediction': {
                '1': '🏠 Home Win',
                'X': '🤝 Draw',
                '2': '✈️ Away Win'
            }.get(best_prediction, 'Unknown'),
            'best_odds': {
                '1': odds_1,
                'X': odds_x,
                '2': odds_2
            }.get(best_prediction, 0),
            'best_win_rate': best_rate,
            'best_upset_rate': best_analysis['upset_rate'],
            'prediction_summary': {
                '1': {'win_rate': analysis_1['win_rate'], 'upset_rate': analysis_1['upset_rate'], 'btts': analysis_1['btts_rate']},
                'X': {'win_rate': analysis_x['win_rate'], 'upset_rate': analysis_x['upset_rate'], 'btts': analysis_x['btts_rate']},
                '2': {'win_rate': analysis_2['win_rate'], 'upset_rate': analysis_2['upset_rate'], 'btts': analysis_2['btts_rate']}
            },
            'average_confidence': int((analysis_1['confidence'] + analysis_x['confidence'] + analysis_2['confidence']) / 3),
            'rationale': rationale,
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        app.logger.error(f'Error in api_predict: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def api_upload():
    """
    API endpoint to upload screenshots and auto-extract predictions
    Request: POST /api/upload (multipart/form-data)
    Files: file (one or multiple images)
    
    Returns: {
        "success": true,
        "count": 2,
        "results": [
            {
                "filename": "screenshot.png",
                "match": "Man City vs Brighton",
                "odds_1": 1.40,
                "odds_x": 3.20,
                "odds_2": 7.00,
                "home_team": "Man City",
                "away_team": "Brighton",
                "source": "Betpawa",
                "historical_win_rate": 62.5,
                "upset_rate": 32.0,
                "btts_rate": 45.0,
                "confidence": 80,
                "prediction": "🏠 Home Win",
                "rationale": "..."
            }
        ]
    }
    """
    
    # Check if Tesseract OCR is available
    if not HAS_PYTESSERACT:
        return jsonify({
            'success': False,
            'error': 'OCR Engine Not Installed',
            'message': 'Pytesseract is not installed on this system',
            'solution': 'Install OCR: pip install pytesseract',
            'tesseract_required': True
        }), 501
    
    # Check if Tesseract binary exists
    try:
        import shutil
        if not shutil.which('tesseract'):
            return jsonify({
                'success': False,
                'error': 'Tesseract OCR Binary Not Found',
                'message': 'Tesseract OCR engine is not installed or not in PATH',
                'solution': 'Download and install from: https://github.com/UB-Mannheim/tesseract/wiki',
                'tesseract_required': True,
                'status': 'MISSING_BINARY'
            }), 501
    except:
        pass  # Continue anyway if shutil.which fails
    
    try:
        if 'file' not in request.files:
            app.logger.warning('API upload called with no file')
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        files = request.files.getlist('file')
        if not files or files[0].filename == '':
            app.logger.warning('API upload called with no selected file')
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        app.logger.info(f'API upload initiated: {len(files)} file(s)')
        results = []
        errors = []
        
        for file in files:
            if not allowed_file(file.filename):
                warning_msg = f'{file.filename}: Invalid file type (PNG, JPG, GIF, BMP only)'
                app.logger.warning(warning_msg)
                errors.append(warning_msg)
                continue
            
            try:
                # Save file
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                filename = timestamp + filename
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # Extract odds from image
                extraction = extract_odds_from_image(filepath)
                
                if not extraction.get('success') or not extraction.get('extracted_odds'):
                    errors.append(f'{file.filename}: Could not extract odds from image')
                    continue
                
                # Get extracted data
                extracted_odds = extraction.get('extracted_odds', {})
                odds_1 = extracted_odds.get('odds_1', 0)
                odds_x = extracted_odds.get('odds_x', 0)
                odds_2 = extracted_odds.get('odds_2', 0)
                
                if not all([odds_1, odds_x, odds_2]):
                    errors.append(f'{file.filename}: Missing some odds (need 1, X, and 2)')
                    continue
                
                home_team = extraction.get('home_team', 'Unknown')
                away_team = extraction.get('away_team', 'Unknown')
                match_name = extraction.get('match_name', f'{home_team} vs {away_team}')
                source = extraction.get('source', 'Unknown')
                
                # Run predictions
                analysis_1 = analyze_odds_range(odds_1, '1')
                analysis_x = analyze_odds_range(odds_x, 'X')
                analysis_2 = analyze_odds_range(odds_2, '2')
                
                # Find best prediction
                predictions = [
                    ('1', analysis_1['win_rate'], analysis_1),
                    ('X', analysis_x['win_rate'], analysis_x),
                    ('2', analysis_2['win_rate'], analysis_2)
                ]
                best_pred, best_rate, best_analysis = max(predictions, key=lambda x: x[1])
                
                pred_display = {
                    '1': '🏠 Home Win',
                    'X': '🤝 Draw',
                    '2': '✈️ Away Win'
                }.get(best_pred, 'Unknown')
                
                # Generate rationale
                rationale_parts = []
                if best_rate > 55:
                    rationale_parts.append(f"Strong: {best_rate}% historical win rate")
                elif best_rate > 45:
                    rationale_parts.append(f"Moderate: {best_rate}% historical win rate")
                
                if best_analysis['upset_rate'] > 30:
                    if best_analysis['is_favorite']:
                        rationale_parts.append(f"Favorite risk: {best_analysis['upset_rate']}%")
                    else:
                        rationale_parts.append(f"Underdog opportunity: {best_analysis['upset_rate']}%")
                
                if best_analysis['btts_rate'] > 55:
                    rationale_parts.append(f"BTTS High: {best_analysis['btts_rate']}%")
                
                if best_analysis['confidence'] >= 80:
                    rationale_parts.append(f"High confidence: {best_analysis['confidence']}%")
                elif best_analysis['sample_size'] < 3:
                    rationale_parts.append(f"Low data: {best_analysis['sample_size']} matches")
                
                rationale = " | ".join(rationale_parts) if rationale_parts else "Based on historical odds ranges"
                
                results.append({
                    'filename': file.filename,
                    'match': match_name,
                    'odds_1': round(odds_1, 2),
                    'odds_x': round(odds_x, 2),
                    'odds_2': round(odds_2, 2),
                    'odds_display': f"{round(odds_1, 2)} / {round(odds_x, 2)} / {round(odds_2, 2)}",
                    'home_team': home_team,
                    'away_team': away_team,
                    'source': source,
                    'odds_category': best_analysis['category'],
                    'historical_win_rate': best_rate,
                    'upset_rate': best_analysis['upset_rate'],
                    'btts_rate': best_analysis['btts_rate'],
                    'confidence': best_analysis['confidence'],
                    'sample_size': best_analysis['sample_size'],
                    'prediction': pred_display,
                    'prediction_short': best_pred,
                    'best_odds': {
                        '1': odds_1,
                        'X': odds_x,
                        '2': odds_2
                    }.get(best_pred, 0),
                    'rationale': rationale,
                    'is_favorite': best_analysis['is_favorite'],
                    'uploaded_at': datetime.now().isoformat()
                })
                
            except Exception as file_error:
                app.logger.error(f'Error processing {file.filename}: {str(file_error)}', exc_info=True)
                errors.append(f'{file.filename}: {str(file_error)}')
                try:
                    db.session.rollback()
                except:
                    pass
                continue
        
        if not results:
            return jsonify({
                'success': False,
                'error': 'No valid images processed',
                'errors': errors
            }), 400
        
        return jsonify({
            'success': True,
            'count': len(results),
            'results': results,
            'errors': errors if errors else [],
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }), 200
        
    except Exception as e:
        app.logger.error(f'Error in api_upload: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    # Use environment variables for configuration
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    
    if not debug_mode:
        app.logger.info(f'Starting Flask app on {host}:{port} (production mode)')
    
    app.run(debug=debug_mode, host=host, port=port)
