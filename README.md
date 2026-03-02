# Football Odds Predictor 🎯⚽

A free web application that allows you to upload football betting odds screenshots from Betpawa and 1xbet, analyze them with AI, and predict upcoming odds movements. Perfect for sharing predictions on Facebook and earning affiliate commissions!

## Features ✨

- **Image Upload & OCR**: Upload screenshots of odds from Betpawa or 1xbet
- **AI Odds Extraction**: Automatically extract odds numbers from images using OCR
- **Smart Predictions**: Predict next odds movements based on historical trends
- **History Tracking**: Keep track of all odds over time
- **Analytics Dashboard**: View statistics and patterns
- **Mobile Friendly**: Responsive design works on all devices
- **Zero Cost**: Completely free to use and deploy

## Installation 📦

### Requirements
- Python 3.8+
- Tesseract OCR (for image text extraction)

### Step 1: Install Python Dependencies

```bash
cd football_odds_predictor
pip install -r requirements.txt
```

### Step 2: Install Tesseract OCR

**Windows:**
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer (choose default paths)
3. The app will auto-detect it after restart

**Mac:**
```bash
brew install tesseract
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

### Step 3: Run the Application

```bash
python app.py
```

The application will start at: **http://localhost:5000**

## Usage 🚀

### 1. Upload Odds
- Take screenshot of odds from Betpawa or 1xbet
- Fill in match name and select source
- Upload the image (system will extract odds automatically or you can enter manually)
- Add optional notes

### 2. View History
- All uploaded odds are saved in database
- See full history of all matches and odds
- Compare trends over time

### 3. Get Predictions
- Click "Predict Next" on any record
- System analyzes historical patterns
- Shows predicted odds direction (UP/DOWN) with confidence score

### 4. View Statistics
- Total records uploaded
- Average odds by type
- Breakdown by source (Betpawa/1xbet)

## Monetization Strategy 💰

### Step 1: Build Audience
- Upload predictions regularly to your Facebook page
- Share winning predictions
- Build credibility with your 5k+ followers

### Step 2: Get Affiliate Links
- Sign up as affiliate for:
  - **Bet365**: betaffiliateprogram.com
  - **1xBet**: affiliates.1xbet.com
  - **22bet**: https://affiliates.22bet.com
  - **Betpawa**: Contact their affiliate program
- Get your unique referral links

### Step 3: Create Content
Example Facebook post:
```
🎯 MATCH PREDICTION - Tonight's Games 🎯

Arsenal vs Man City
🏠 Home: 2.50 → Predicted: 2.45 ⬇️
🤝 Draw: 3.20 → Predicted: 3.18 ⬇️  
✈️ Away: 2.80 → Predicted: 2.90 ⬆️

Get started with betting here: [AFFILIATE LINK]
#Football #Predictions #BettingTips
```

### Step 4: Earn Commissions
- Earn 20-40% commission per signup
- More predictions = more followers = more commissions
- Scale by sharing consistently

## Database Schema 🗂️

Records stored with:
- Match name
- Odds for Home (1), Draw (X), Away (2)
- Source (Betpawa/1xbet)
- Screenshot path
- Upload timestamp
- Notes

## API Endpoints 📡

```
POST /upload              - Upload odds image
GET  /history            - Get odds history
GET  /predict/<id>       - Get prediction for match
GET  /stats              - Get platform statistics
DELETE /delete/<id>      - Delete record
GET  /image/<filename>   - Serve uploaded image
```

## Deploying for FREE 🌐

### Option 1: Heroku (Free dyno - limited)
```bash
# Install Heroku CLI, then:
heroku create your-app-name
git push heroku main
```

### Option 2: Replit
1. Upload to Replit
2. Run directly from browser
3. Get public URL instantly
4. Free hosting with 1GB storage

### Option 3: Render.com (Recommended)
1. Push to GitHub
2. Connect to Render
3. Deploy for free with 500 free hours/month
4. Perfect for side projects

### Option 4: PythonAnywhere
1. Create free account
2. Upload files
3. Configure web app
4. Get public URL

## Sharing on Facebook 📱

1. Add link to your website in Facebook bio
2. Share predictions with your followers
3. Include affiliate links (use link shortener like bit.ly first)
4. Post regularly (daily predictions work best)

## Tips for Success 💡

1. **Be Consistent**: Post predictions at same time daily
2. **Track Accuracy**: Share your winning predictions
3. **Engage Community**: Ask followers for their predictions
4. **Educate**: Explain why you predict certain odds
5. **Trust Building**: Start with free predictions
6. **Premium Tier**: Later offer premium for instant predictions

## Income Potential 💵

- **Week 1-2**: Build audience with free predictions
- **Week 3-4**: First affiliate signups (5-10 = $50-500 commission)
- **Month 2**: 20-30 signups = $500-2000
- **Month 3+**: Scale to $2,000-10,000/month with growing audience

*Note: Results depend on content quality and engagement*

## Troubleshooting 🔧

**OCR not working:**
- Check Tesseract is installed
- Verify path: `C:\Program Files\Tesseract-OCR\tesseract.exe` (Windows)

**Images not uploading:**
- Check uploads folder exists
- Verify file size < 16MB
- Ensure image is .jpg, .png, .gif, or .bmp

**Database errors:**
- Delete `odds_history.db` to reset
- Re-run app.py

## Support & Feedback

Having issues? Check:
1. Python version (3.8+)
2. All dependencies installed
3. Tesseract OCR installed
4. Upload folder exists

## License

Free to use and modify for personal/commercial use.

## Future Features 🚀

- Live odds API integration
- Match result tracking for accuracy
- Advanced machine learning predictions
- Multi-language support
- Mobile app
- Telegram bot integration
- Slack notifications

---

**Ready to earn? Start uploading predictions and building your audience today!** 🎯💰

Follow this workflow:
1. Daily: Upload 5-10 odds predictions
2. Weekly: Track accuracy
3. Monthly: Share success stories
4. Scale: Increase affiliate links and monetization

Good luck! 🚀
