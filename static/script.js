// Tab navigation
function showTab(tabName) {
    // Hide all tab content
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.remove('active'));
    
    // Remove active from buttons
    const buttons = document.querySelectorAll('.nav-btn');
    buttons.forEach(btn => btn.classList.remove('active'));
    
    // Show selected tab
    document.getElementById(tabName).classList.add('active');
    
    // Add active to button
    event.target.closest('.nav-btn').classList.add('active');
    
    // Load data if needed
    if (tabName === 'history') {
        loadHistory();
    } else if (tabName === 'predictions') {
        loadPredictions();
    } else if (tabName === 'stats') {
        loadStats();
    }
}

// File input handler with preview for multiple files
document.getElementById('fileInput').addEventListener('change', function(e) {
    handleFileSelect(e.target.files);
});

// Drag and drop handlers for multiple files
const dropZone = document.getElementById('dropZone');

dropZone.addEventListener('dragover', function(e) {
    e.preventDefault();
    e.stopPropagation();
    dropZone.style.borderColor = '#0099cc';
    dropZone.style.backgroundColor = '#e8f4f8';
});

dropZone.addEventListener('dragleave', function(e) {
    e.preventDefault();
    e.stopPropagation();
    dropZone.style.borderColor = '#00d4ff';
    dropZone.style.backgroundColor = '';
});

dropZone.addEventListener('drop', function(e) {
    e.preventDefault();
    e.stopPropagation();
    dropZone.style.borderColor = '#00d4ff';
    dropZone.style.backgroundColor = '';
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        const imageFiles = Array.from(files).filter(file => file.type.startsWith('image/'));
        if (imageFiles.length > 0) {
            // Create a new FileList-like object
            const dt = new DataTransfer();
            imageFiles.forEach(file => dt.items.add(file));
            document.getElementById('fileInput').files = dt.files;
            handleFileSelect(imageFiles);
        } else {
            alert('Please upload image files (JPG, PNG, GIF, BMP)');
        }
    }
});

// Handle multiple file selection and show previews
function handleFileSelect(files) {
    if (!files || files.length === 0) return;
    
    const fileCount = files.length;
    const totalSize = Array.from(files).reduce((sum, file) => sum + file.size, 0);
    const totalSizeMB = (totalSize / 1024 / 1024).toFixed(2);
    
    document.getElementById('fileName').innerHTML = `<strong>${fileCount} file(s) selected</strong> (${totalSizeMB} MB total)`;
    
    // Show image previews
    const previewContainer = document.getElementById('previewContainer');
    const preview = document.getElementById('imagePreview');
    previewContainer.innerHTML = '';
    
    Array.from(files).forEach((file, index) => {
        const reader = new FileReader();
        reader.onload = function(e) {
            const imgWrapper = document.createElement('div');
            imgWrapper.style.cssText = 'position: relative; border: 2px solid #00d4ff; border-radius: 8px; overflow: hidden;';
            
            const img = document.createElement('img');
            img.src = e.target.result;
            img.style.cssText = 'width: 100%; height: 150px; object-fit: cover;';
            
            const filename = document.createElement('div');
            filename.textContent = file.name.substring(0, 20) + (file.name.length > 20 ? '...' : '');
            filename.style.cssText = 'padding: 5px; background: rgba(0,0,0,0.7); color: white; font-size: 0.8em; text-align: center;';
            
            imgWrapper.appendChild(img);
            imgWrapper.appendChild(filename);
            previewContainer.appendChild(imgWrapper);
        };
        reader.readAsDataURL(file);
    });
    
    preview.style.display = 'block';
    document.querySelector('.upload-content').style.display = 'none';
}

// Clear selected images
function clearImage() {
    document.getElementById('fileInput').value = '';
    document.getElementById('fileName').textContent = 'Click to select multiple images or drag & drop here';
    document.getElementById('imagePreview').style.display = 'none';
    document.getElementById('previewContainer').innerHTML = '';
    document.querySelector('.upload-content').style.display = 'block';
}

// Upload form handler for multiple files
document.getElementById('uploadForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const resultDiv = document.getElementById('uploadResult');
    
    const fileCount = document.getElementById('fileInput').files.length;
    
    try {
        resultDiv.className = 'result info show';
        resultDiv.innerHTML = `<i class="fas fa-spinner loading"></i> Uploading and analyzing ${fileCount} file(s)...`;
        
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            let resultsHTML = `
                <h4><i class="fas fa-check-circle"></i> Successfully Processed ${data.count} Screenshot(s)!</h4>
                <p>${data.message}</p>
            `;
            
            // Show each uploaded file's results
            data.results.forEach((result, index) => {
                const pred = result.prediction;
                const extracted = result.extracted_data;
                
                resultsHTML += `
                    <div style="margin-top: 20px; padding: 20px; background: #f9f9f9; border-radius: 10px; border-left: 5px solid #00d4ff;">
                        <h3 style="margin-top: 0; color: #0099cc;">
                            📄 File ${index + 1}: ${result.filename}
                        </h3>
                        
                        <div style="background: white; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
                            <strong>🤖 AI Extracted Data:</strong>
                            <ul style="margin: 10px 0; line-height: 1.8;">
                                <li><strong>Teams:</strong> ${result.teams}</li>
                                <li><strong>Odds:</strong> 1: ${extracted.odds_1 || 'N/A'} | X: ${extracted.odds_x || 'N/A'} | 2: ${extracted.odds_2 || 'N/A'}</li>
                                <li><strong>Source:</strong> ${extracted.source}</li>
                                <li><strong>Confidence:</strong> ${extracted.confidence}%</li>
                            </ul>
                        </div>
                `;
                
                // Show prediction if available
                if (pred && !pred.error && pred.recommended_bet) {
                    const betName = pred.recommended_bet === '1' ? 'Home Win (1)' : 
                                   pred.recommended_bet === 'X' ? 'Draw (X)' : 'Away Win (2)';
                    resultsHTML += `
                        <div style="background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%); 
                                    color: white; padding: 20px; border-radius: 10px;">
                            <h4 style="margin: 0 0 10px 0;"><i class="fas fa-trophy"></i> RECOMMENDED BET</h4>
                            <div style="font-size: 1.6em; font-weight: bold; margin: 10px 0;">
                                ${betName}
                            </div>
                            <div style="font-size: 1.1em;">
                                Win Rate: ${pred.recommended_bet_rate}% 
                                (${pred.total_completed_matches} matches analyzed)
                            </div>
                        </div>
                        
                        <div style="margin-top: 15px; background: white; padding: 15px; border-radius: 8px;">
                            <strong>📊 Historical Win Rates:</strong>
                            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 10px;">
                                <div style="text-align: center; padding: 10px; background: #f9f9f9; border-radius: 5px;">
                                    <div style="font-weight: bold;">Home Win</div>
                                    <div style="font-size: 1.5em; color: #00d4ff;">${pred.win_rate_1}%</div>
                                </div>
                                <div style="text-align: center; padding: 10px; background: #f9f9f9; border-radius: 5px;">
                                    <div style="font-weight: bold;">Draw</div>
                                    <div style="font-size: 1.5em; color: #00d4ff;">${pred.win_rate_x}%</div>
                                </div>
                                <div style="text-align: center; padding: 10px; background: #f9f9f9; border-radius: 5px;">
                                    <div style="font-weight: bold;">Away Win</div>
                                    <div style="font-size: 1.5em; color: #00d4ff;">${pred.win_rate_2}%</div>
                                </div>
                            </div>
                        </div>
                    `;
                    
                    if (pred.team_specific) {
                        resultsHTML += `
                            <div style="margin-top: 10px; padding: 10px; background: #fff3cd; border-radius: 5px;">
                                <strong>🎯 Team-Specific:</strong> ${pred.team_specific.matches_found} matches found<br>
                                <small>Home: ${pred.team_specific.win_rate_1}% | Draw: ${pred.team_specific.win_rate_x}% | Away: ${pred.team_specific.win_rate_2}%</small>
                            </div>
                        `;
                    }
                } else if (pred && pred.total_completed_matches === 0) {
                    resultsHTML += `
                        <div style="padding: 15px; background: #fff3cd; border-radius: 8px;">
                            <strong>💡 Tip:</strong> Mark match results in History tab to enable predictions!
                        </div>
                    `;
                }
                
                resultsHTML += `</div>`;
            });
            
            // Show errors if any
            if (data.errors && data.errors.length > 0) {
                resultsHTML += `
                    <div style="margin-top: 15px; padding: 15px; background: #fff3cd; border-radius: 8px;">
                        <strong>⚠️ Some files had issues:</strong>
                        <ul style="margin: 10px 0;">
                            ${data.errors.map(err => `<li>${err}</li>`).join('')}
                        </ul>
                    </div>
                `;
            }
            
            resultsHTML += `
                <div style="margin-top: 20px; text-align: center;">
                    <button class="btn btn-primary" onclick="location.reload()">
                        <i class="fas fa-plus"></i> Upload More Screenshots
                    </button>
                    <button class="btn btn-secondary" onclick="showTab('history'); event.stopPropagation();" style="margin-left: 10px;">
                        <i class="fas fa-history"></i> View History
                    </button>
                </div>
            `;
            
            resultDiv.className = 'result success show';
            resultDiv.innerHTML = resultsHTML;
            
            // Clear form
            document.getElementById('uploadForm').reset();
            clearImage();
        } else {
            resultDiv.className = 'result error show';
            resultDiv.innerHTML = `
                <h4><i class="fas fa-times-circle"></i> Upload Failed</h4>
                <p>${data.error || 'Unknown error occurred'}</p>
                ${data.errors ? `<ul>${data.errors.map(e => `<li>${e}</li>`).join('')}</ul>` : ''}
            `;
        }
    } catch (error) {
        resultDiv.className = 'result error show';
        resultDiv.innerHTML = `
            <h4><i class="fas fa-times-circle"></i> Error</h4>
            <p>${error.message}</p>
        `;
    }
});

// Load history
async function loadHistory() {
    try {
        const response = await fetch('/history?limit=20');
        const data = await response.json();
        
        const container = document.getElementById('historyContainer');
        
        if (!data.records || data.records.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-inbox"></i>
                    <p>No odds records yet. Upload your first screenshot to get started!</p>
                </div>
            `;
            return;
        }
        
        container.innerHTML = data.records.map(record => {
            // Build result status badge
            let resultBadge = '';
            if (record.is_completed && record.actual_result) {
                const resultText = record.actual_result === '1' ? 'Home Win ✓' : 
                                  record.actual_result === 'X' ? 'Draw ✓' : 'Away Win ✓';
                resultBadge = `<span style="background: #28a745; color: white; padding: 3px 10px; border-radius: 20px; font-size: 0.8em; margin-left: 10px;">${resultText}</span>`;
            } else {
                resultBadge = `<span style="background: #ffc107; color: #333; padding: 3px 10px; border-radius: 20px; font-size: 0.8em; margin-left: 10px;">⏳ Pending</span>`;
            }
            
            // Build result buttons
            let resultButtons = '';
            if (!record.is_completed) {
                resultButtons = `
                    <div style="margin-top: 10px; padding: 10px; background: #f9f9f9; border-radius: 5px;">
                        <strong>📝 Mark Result:</strong>
                        <div style="display: flex; gap: 5px; margin-top: 5px;">
                            <button class="btn btn-secondary" onclick="updateResult(${record.id}, '1')" style="flex: 1; font-size: 0.9em;">
                                1 (Home)
                            </button>
                            <button class="btn btn-secondary" onclick="updateResult(${record.id}, 'X')" style="flex: 1; font-size: 0.9em;">
                                X (Draw)
                            </button>
                            <button class="btn btn-secondary" onclick="updateResult(${record.id}, '2')" style="flex: 1; font-size: 0.9em;">
                                2 (Away)
                            </button>
                        </div>
                    </div>
                `;
            }
            
            return `
                <div class="record-card">
                    <div class="record-header">
                        <div>
                            <div class="record-title">${record.match_name}${resultBadge}</div>
                            <span class="record-source">${record.source}</span>
                            <div class="record-time"><i class="fas fa-clock"></i> ${record.uploaded_at}</div>
                        </div>
                    </div>
                    <div class="odds-display">
                        <div class="odd-item">
                            <div class="odd-label">Home (1)</div>
                            <div class="odd-value">${record.odds_1 ? record.odds_1.toFixed(2) : 'N/A'}</div>
                        </div>
                        <div class="odd-item">
                            <div class="odd-label">Draw (X)</div>
                            <div class="odd-value">${record.odds_x ? record.odds_x.toFixed(2) : 'N/A'}</div>
                        </div>
                        <div class="odd-item">
                            <div class="odd-label">Away (2)</div>
                            <div class="odd-value">${record.odds_2 ? record.odds_2.toFixed(2) : 'N/A'}</div>
                        </div>
                    </div>
                    ${record.notes ? `<div class="record-note"><strong>Notes:</strong> ${record.notes}</div>` : ''}
                    ${resultButtons}
                    <div class="record-actions">
                        <button class="btn btn-secondary" onclick="predictOdds(${record.id})">
                            <i class="fas fa-crystal-ball"></i> Predict Next
                        </button>
                        <button class="btn btn-danger" onclick="deleteRecord(${record.id})">
                            <i class="fas fa-trash"></i> Delete
                        </button>
                    </div>
                </div>
            `;
        }).join('');
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

// Load predictions
async function loadPredictions() {
    try {
        const response = await fetch('/history?limit=20');
        const data = await response.json();
        
        const container = document.getElementById('predictionsContainer');
        
        if (!data.records || data.records.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-crystal-ball"></i>
                    <p>Upload odds records to generate predictions</p>
                </div>
            `;
            return;
        }
        
        // Load predictions for all records
        let predictions = [];
        for (const record of data.records.slice(0, 10)) {
            try {
                const predResponse = await fetch(`/predict/${record.id}`);
                const predData = await predResponse.json();
                if (predData.prediction && !predData.prediction.error) {
                    predictions.push({
                        ...record,
                        prediction: predData.prediction
                    });
                }
            } catch (e) {
                console.log('No prediction for', record.id);
            }
        }
        
        if (predictions.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-info-circle"></i>
                    <p>Need at least 2 records from the same source to generate predictions</p>
                </div>
            `;
            return;
        }
        
        container.innerHTML = predictions.map(item => `
            <div class="prediction-card">
                <div class="record-header">
                    <div>
                        <div class="record-title">${item.match_name}</div>
                        <span class="record-source">${item.source}</span>
                    </div>
                </div>
                <div style="margin-bottom: 15px;">
                    <strong>Current Odds:</strong>
                    <div class="odds-display">
                        <div class="odd-item">
                            <div class="odd-label">Home (1)</div>
                            <div class="odd-value">${item.odds_1 ? item.odds_1.toFixed(2) : 'N/A'}</div>
                        </div>
                        <div class="odd-item">
                            <div class="odd-label">Draw (X)</div>
                            <div class="odd-value">${item.odds_x ? item.odds_x.toFixed(2) : 'N/A'}</div>
                        </div>
                        <div class="odd-item">
                            <div class="odd-label">Away (2)</div>
                            <div class="odd-value">${item.odds_2 ? item.odds_2.toFixed(2) : 'N/A'}</div>
                        </div>
                    </div>
                </div>
                <div style="margin-bottom: 15px;">
                    <strong>Predicted Next Odds:</strong>
                    <div class="odds-display">
                        <div class="odd-item">
                            <div class="odd-label">Home (1)</div>
                            <div class="odd-value">${item.prediction.odds_1_prediction || 'N/A'}</div>
                            <div class="trend ${item.prediction.odds_1_trend === 'UP' ? 'up' : 'down'}">
                                <i class="fas fa-arrow-${item.prediction.odds_1_trend === 'UP' ? 'up' : 'down'}"></i>
                                ${item.prediction.odds_1_trend}
                            </div>
                        </div>
                        <div class="odd-item">
                            <div class="odd-label">Draw (X)</div>
                            <div class="odd-value">${item.prediction.odds_x_prediction || 'N/A'}</div>
                            <div class="trend ${item.prediction.odds_x_trend === 'UP' ? 'up' : 'down'}">
                                <i class="fas fa-arrow-${item.prediction.odds_x_trend === 'UP' ? 'up' : 'down'}"></i>
                                ${item.prediction.odds_x_trend}
                            </div>
                        </div>
                        <div class="odd-item">
                            <div class="odd-label">Away (2)</div>
                            <div class="odd-value">${item.prediction.odds_2_prediction || 'N/A'}</div>
                            <div class="trend ${item.prediction.odds_2_trend === 'UP' ? 'up' : 'down'}">
                                <i class="fas fa-arrow-${item.prediction.odds_2_trend === 'UP' ? 'up' : 'down'}"></i>
                                ${item.prediction.odds_2_trend}
                            </div>
                        </div>
                    </div>
                </div>
                <div style="background: #f0f0f0; padding: 10px; border-radius: 5px; text-align: center;">
                    <strong>Confidence:</strong> ${item.prediction.confidence || 0}%
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading predictions:', error);
    }
}

// Load statistics
async function loadStats() {
    try {
        const response = await fetch('/stats');
        const data = await response.json();
        
        const container = document.getElementById('statsContainer');
        
        let statsHTML = `
            <div class="stat-box">
                <div class="stat-label">Total Records</div>
                <div class="stat-value">${data.total_records}</div>
            </div>
            <div class="stat-box secondary">
                <div class="stat-label">Completed Matches</div>
                <div class="stat-value">${data.completed_matches || 0}</div>
            </div>
            <div class="stat-box tertiary">
                <div class="stat-label">Pending Matches</div>
                <div class="stat-value">${data.pending_matches || 0}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Betpawa Records</div>
                <div class="stat-value">${data.betpawa_count}</div>
            </div>
            <div class="stat-box secondary">
                <div class="stat-label">1xbet Records</div>
                <div class="stat-value">${data.one_xbet_count}</div>
            </div>
        `;
        
        // Add win rates if available
        if (data.win_rates) {
            statsHTML += `
                <div class="stat-box" style="grid-column: 1 / -1; background: linear-gradient(135deg, #28a745 0%, #20c997 100%);">
                    <div class="stat-label" style="font-size: 1.2em; margin-bottom: 10px;">🏆 WIN RATE ANALYSIS</div>
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; text-align: center;">
                        <div>
                            <div style="font-size: 2em; font-weight: bold;">${data.win_rates.home_wins}%</div>
                            <div>Home Wins (1)</div>
                        </div>
                        <div>
                            <div style="font-size: 2em; font-weight: bold;">${data.win_rates.draws}%</div>
                            <div>Draws (X)</div>
                        </div>
                        <div>
                            <div style="font-size: 2em; font-weight: bold;">${data.win_rates.away_wins}%</div>
                            <div>Away Wins (2)</div>
                        </div>
                    </div>
                    <div style="margin-top: 10px; font-size: 0.9em;">Based on ${data.win_rates.total_analyzed} completed matches</div>
                </div>
            `;
        } else {
            statsHTML += `
                <div class="stat-box" style="grid-column: 1 / -1; background: #ffc107;">
                    <div class="stat-label">💡 Upload Match Results</div>
                    <div style="margin-top: 10px;">Mark completed matches to see win rate analysis and improve predictions!</div>
                </div>
            `;
        }
        
        container.innerHTML = statsHTML;
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Predict odds for a specific match
async function predictOdds(matchId) {
    try {
        const response = await fetch(`/predict/${matchId}`);
        const data = await response.json();
        
        if (data.prediction && !data.prediction.error) {
            alert(`
Prediction for: ${data.match_name}
Confidence: ${data.prediction.confidence}%

Next Predicted Odds:
1 (Home): ${data.prediction.odds_1_prediction} (${data.prediction.odds_1_trend})
X (Draw): ${data.prediction.odds_x_prediction} (${data.prediction.odds_x_trend})
2 (Away): ${data.prediction.odds_2_prediction} (${data.prediction.odds_2_trend})

Based on ${data.history_count} historical records from ${data.current_odds.source}
            `);
        } else {
            alert('Unable to generate prediction. Need more historical data for this source.');
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

// Delete record
async function deleteRecord(recordId) {
    if (!confirm('Are you sure you want to delete this record?')) {
        return;
    }
    
    try {
        const response = await fetch(`/delete/${recordId}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert('Record deleted successfully');
            loadHistory();
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

// Update match result
async function updateResult(recordId, result) {
    if (!confirm(`Mark this match result as: ${result === '1' ? 'Home Win (1)' : result === 'X' ? 'Draw (X)' : 'Away Win (2)'}?`)) {
        return;
    }
    
    try {
        const response = await fetch(`/update_result/${recordId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ result: result })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert('✅ Match result updated! Future predictions will use this data.');
            loadHistory();
            loadStats();  // Refresh stats to show updated win rates
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

// Load odds analysis report with value bet detection
async function loadOddsReport() {
    try {
        const source = document.getElementById('analysisSource').value;
        const container = document.getElementById('analysisContainer');
        container.innerHTML = '<p style="text-align: center;"><i class="fas fa-spinner loading"></i> Generating Odds Analysis Report...</p>';
        
        const url = source ? `/odds-report?source=${source}` : '/odds-report';
        const response = await fetch(url);
        const data = await response.json();
        
        if (!response.ok || data.error) {
            container.innerHTML = `<p style="text-align: center; color: #d9534f;">Error: ${data.error || 'Failed to load report'}</p>`;
            return;
        }
        
        if (!data.report || data.report.length === 0) {
            container.innerHTML = '<p style="text-align: center; color: #999;">No matches to analyze. Upload odds first!</p>';
            return;
        }
        
        // Build enhanced table
        let html = `
            <table style="width: 100%; border-collapse: collapse; background: white;">
                <thead style="background: linear-gradient(135deg, #0099cc 0%, #00d4ff 100%); color: white; font-weight: bold;">
                    <tr>
                        <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Match</th>
                        <th style="padding: 12px; text-align: center; border: 1px solid #ddd;">Status</th>
                        <th style="padding: 12px; text-align: center; border: 1px solid #ddd;">Odds</th>
                        <th style="padding: 12px; text-align: center; border: 1px solid #ddd;">Category</th>
                        <th style="padding: 12px; text-align: center; border: 1px solid #ddd;">Prediction</th>
                        <th style="padding: 12px; text-align: center; border: 1px solid #ddd;">Win %</th>
                        <th style="padding: 12px; text-align: center; border: 1px solid #ddd;">Upset %</th>
                        <th style="padding: 12px; text-align: center; border: 1px solid #ddd;">BTTS %</th>
                        <th style="padding: 12px; text-align: center; border: 1px solid #ddd;">Confidence</th>
                        <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Rationale & Value</th>
                    </tr>
                </thead>
                <tbody>
        `;
        
        data.report.forEach(match => {
            const statusColor = match.status.includes('COMPLETE') ? '#28a745' : '#ffc107';
            const statusTextColor = match.status.includes('COMPLETE') ? 'white' : '#333';
            
            // Highlight value bets
            const valueBetBg = match.is_value_opportunity ? 'linear-gradient(135deg, #fff3cd 0%, #ffe8a1 100%)' : 'white';
            const valueBetBorder = match.is_value_opportunity ? '3px solid #ffc107' : '1px solid #ddd';
            
            const confidenceColor = match.confidence >= 80 ? '#28a745' : (match.confidence >= 60 ? '#ffc107' : '#d9534f');
            const upsetColor = match.upset_rate > 30 ? '#d9534f' : '#17a2b8';
            
            html += `
                <tr style="background: ${valueBetBg}; border-left: ${valueBetBorder}; transition: all 0.3s ease;">
                    <td style="padding: 12px; border: 1px solid #ddd;">
                        <strong>${match.match}</strong><br>
                        <small style="color: #666;">${match.source} • ${match.uploaded_at}</small>
                    </td>
                    <td style="padding: 12px; border: 1px solid #ddd; text-align: center;">
                        <span style="background: ${statusColor}; color: ${statusTextColor}; padding: 5px 10px; border-radius: 20px; font-size: 0.85em; font-weight: bold;">
                            ${match.status}
                        </span>
                    </td>
                    <td style="padding: 12px; border: 1px solid #ddd; text-align: center; font-family: 'Courier New'; font-size: 0.9em;">
                        <strong>${match.odds_1.toFixed(2)}</strong> / ${match.odds_x.toFixed(2)} / ${match.odds_2.toFixed(2)}<br>
                        <small style="color: #999;">${match.odds_range}</small>
                    </td>
                    <td style="padding: 12px; border: 1px solid #ddd; text-align: center; font-size: 0.85em; color: #666;">
                        ${match.is_favorite ? '⚡ Fav' : '🎯 Dog'}
                    </td>
                    <td style="padding: 12px; border: 1px solid #ddd; text-align: center; font-weight: bold;">
                        ${match.best_prediction}
                        <br><small style="color: #0099cc;">@${match.best_odds.toFixed(2)}</small>
                    </td>
                    <td style="padding: 12px; border: 1px solid #ddd; text-align: center;">
                        <span style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white; padding: 6px 10px; border-radius: 5px; font-weight: bold; font-size: 0.9em;">
                            ${match.historical_win_rate.toFixed(1)}%
                        </span>
                    </td>
                    <td style="padding: 12px; border: 1px solid #ddd; text-align: center;">
                        <span style="background: ${upsetColor}; color: white; padding: 6px 10px; border-radius: 5px; font-weight: bold; font-size: 0.9em;">
                            ${match.upset_rate.toFixed(1)}%
                        </span>
                    </td>
                    <td style="padding: 12px; border: 1px solid #ddd; text-align: center;">
                        <span style="color: ${match.btts_rate > 55 ? '#e74c3c' : '#666'}; font-weight: ${match.btts_rate > 55 ? 'bold' : 'normal'};">
                            ${match.btts_rate.toFixed(1)}%
                        </span>
                    </td>
                    <td style="padding: 12px; border: 1px solid #ddd; text-align: center;">
                        <div style="width: 50px; height: 6px; background: #e0e0e0; border-radius: 10px; margin: 0 auto 5px; overflow: hidden;">
                            <div style="width: ${match.confidence}%; height: 100%; background: ${confidenceColor}; transition: width 0.3s;"></div>
                        </div>
                        <small>${match.confidence.toFixed(0)}%</small>
                    </td>
                    <td style="padding: 12px; border: 1px solid #ddd; font-size: 0.85em; line-height: 1.5;">
                        ${match.is_value_opportunity ? '<strong style="color: #d4af37;">💎 VALUE BET!</strong><br>' : ''}
                        ${match.rationale}
                    </td>
                </tr>
            `;
        });
        
        html += `
                </tbody>
            </table>
            <div style="margin-top: 20px; padding: 15px; background: #e8f4f8; border-radius: 8px;">
                <strong>📊 Report Summary:</strong>
                <ul style="margin: 10px 0; padding-left: 20px;">
                    <li><strong>Total Matches Analyzed:</strong> ${data.total_matches}</li>
                    <li><strong>Value Bets Found:</strong> ${data.report.filter(m => m.is_value_opportunity).length}</li>
                    <li><strong>High Confidence (80%+):</strong> ${data.report.filter(m => m.confidence >= 80).length}</li>
                    <li><strong>Report Generated:</strong> ${data.generated_at}</li>
                </ul>
            </div>
        `;
        
        container.innerHTML = html;
    } catch (error) {
        document.getElementById('analysisContainer').innerHTML = `
            <p style="text-align: center; color: #d9534f;">
                <i class="fas fa-exclamation-circle"></i> Error: ${error.message}
            </p>
        `;
    }
}

// Update tab navigation to include analysis tab
window.addEventListener('load', function() {
    // Override showTab to handle analysis tab
    const originalShowTab = window.showTab;
    window.showTab = function(tabName) {
        // Hide all tab content
        const tabs = document.querySelectorAll('.tab-content');
        tabs.forEach(tab => tab.classList.remove('active'));
        
        // Remove active from buttons
        const buttons = document.querySelectorAll('.nav-btn');
        buttons.forEach(btn => btn.classList.remove('active'));
        
        // Show selected tab
        document.getElementById(tabName).classList.add('active');
        
        // Add active to button
        event.target?.closest?.('.nav-btn')?.classList?.add('active');
        
        // Load data if needed
        if (tabName === 'history') {
            loadHistory();
        } else if (tabName === 'predictions') {
            loadPredictions();
        } else if (tabName === 'stats') {
            loadStats();
        } else if (tabName === 'analysis') {
            loadOddsReport();
        }
    };
    
    // Load stats on page load
    loadStats();
});

// ============================================
// API PREDICT: Handle text-based odds analysis
// ============================================

document.getElementById('apiPredictForm')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const prompt = document.getElementById('predictPrompt').value.trim();
    const resultDiv = document.getElementById('apiPredictResult');
    
    if (!prompt) {
        alert('Please enter odds (e.g., "1.8 vs 4.0")');
        return;
    }
    
    try {
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = '<div style="text-align: center;"><i class="fas fa-spinner loading"></i> Analyzing odds...</div>';
        
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({prompt: prompt})
        });
        
        const data = await response.json();
        
        if (!data.success) {
            resultDiv.innerHTML = `<div style="padding: 15px; background: #f8d7da; border-radius: 5px; color: #721c24;"><strong>Error:</strong> ${data.error}</div>`;
            return;
        }
        
        // Build results table
        let html = `
            <div style="margin-top: 20px;">
                <h3 style="margin-bottom: 15px;">📊 Analysis Results</h3>
                <table style="width: 100%; border-collapse: collapse; background: white;">
                    <thead style="background: linear-gradient(135deg, #0099cc 0%, #00d4ff 100%); color: white;">
                        <tr>
                            <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Metric</th>
                            <th style="padding: 12px; text-align: center; border: 1px solid #ddd;">Home (1)</th>
                            <th style="padding: 12px; text-align: center; border: 1px solid #ddd;">Draw (X)</th>
                            <th style="padding: 12px; text-align: center; border: 1px solid #ddd;">Away (2)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td style="padding: 12px; border: 1px solid #ddd; font-weight: bold;">Odds</td>
                            <td style="padding: 12px; border: 1px solid #ddd; text-align: center; font-family: monospace; font-size: 0.95em;">${data.odds_1}</td>
                            <td style="padding: 12px; border: 1px solid #ddd; text-align: center; font-family: monospace; font-size: 0.95em;">${data.odds_x}</td>
                            <td style="padding: 12px; border: 1px solid #ddd; text-align: center; font-family: monospace; font-size: 0.95em;">${data.odds_2}</td>
                        </tr>
                        <tr>
                            <td style="padding: 12px; border: 1px solid #ddd; font-weight: bold;">Category</td>
                            <td style="padding: 12px; border: 1px solid #ddd; text-align: center; font-size: 0.9em;">${data.analysis_1.category}</td>
                            <td style="padding: 12px; border: 1px solid #ddd; text-align: center; font-size: 0.9em;">Draw</td>
                            <td style="padding: 12px; border: 1px solid #ddd; text-align: center; font-size: 0.9em;">${data.analysis_2.category}</td>
                        </tr>
                        <tr>
                            <td style="padding: 12px; border: 1px solid #ddd; font-weight: bold;">Win %</td>
                            <td style="padding: 12px; border: 1px solid #ddd; text-align: center;"><span style="background: #28a745; color: white; padding: 5px 10px; border-radius: 5px; font-weight: bold;">${data.analysis_1.win_rate.toFixed(1)}%</span></td>
                            <td style="padding: 12px; border: 1px solid #ddd; text-align: center;"><span style="background: #17a2b8; color: white; padding: 5px 10px; border-radius: 5px; font-weight: bold;">${data.analysis_x.win_rate.toFixed(1)}%</span></td>
                            <td style="padding: 12px; border: 1px solid #ddd; text-align: center;"><span style="background: #ffc107; color: #333; padding: 5px 10px; border-radius: 5px; font-weight: bold;">${data.analysis_2.win_rate.toFixed(1)}%</span></td>
                        </tr>
                        <tr>
                            <td style="padding: 12px; border: 1px solid #ddd; font-weight: bold;">Upset %</td>
                            <td style="padding: 12px; border: 1px solid #ddd; text-align: center; color: ${data.analysis_1.upset_rate > 30 ? '#d9534f' : '#666'};">${data.analysis_1.upset_rate.toFixed(1)}%</td>
                            <td style="padding: 12px; border: 1px solid #ddd; text-align: center; color: #666;">${data.analysis_x.upset_rate.toFixed(1)}%</td>
                            <td style="padding: 12px; border: 1px solid #ddd; text-align: center; color: ${data.analysis_2.upset_rate > 30 ? '#28a745' : '#666'};">${data.analysis_2.upset_rate.toFixed(1)}%</td>
                        </tr>
                        <tr>
                            <td style="padding: 12px; border: 1px solid #ddd; font-weight: bold;">BTTS %</td>
                            <td style="padding: 12px; border: 1px solid #ddd; text-align: center;">${data.analysis_1.btts_rate.toFixed(1)}%</td>
                            <td style="padding: 12px; border: 1px solid #ddd; text-align: center;">${data.analysis_x.btts_rate.toFixed(1)}%</td>
                            <td style="padding: 12px; border: 1px solid #ddd; text-align: center;">${data.analysis_2.btts_rate.toFixed(1)}%</td>
                        </tr>
                        <tr>
                            <td style="padding: 12px; border: 1px solid #ddd; font-weight: bold;">Confidence</td>
                            <td style="padding: 12px; border: 1px solid #ddd; text-align: center;">
                                <div style="width: 60px; height: 8px; background: #e0e0e0; border-radius: 5px; margin: 0 auto 5px; overflow: hidden;">
                                    <div style="width: ${data.analysis_1.confidence}%; height: 100%; background: ${data.analysis_1.confidence >= 80 ? '#28a745' : '#ffc107'};"></div>
                                </div>
                                ${data.analysis_1.confidence}%
                            </td>
                            <td style="padding: 12px; border: 1px solid #ddd; text-align: center;">
                                <div style="width: 60px; height: 8px; background: #e0e0e0; border-radius: 5px; margin: 0 auto 5px; overflow: hidden;">
                                    <div style="width: ${data.analysis_x.confidence}%; height: 100%; background: ${data.analysis_x.confidence >= 80 ? '#28a745' : '#ffc107'};"></div>
                                </div>
                                ${data.analysis_x.confidence}%
                            </td>
                            <td style="padding: 12px; border: 1px solid #ddd; text-align: center;">
                                <div style="width: 60px; height: 8px; background: #e0e0e0; border-radius: 5px; margin: 0 auto 5px; overflow: hidden;">
                                    <div style="width: ${data.analysis_2.confidence}%; height: 100%; background: ${data.analysis_2.confidence >= 80 ? '#28a745' : '#ffc107'};"></div>
                                </div>
                                ${data.analysis_2.confidence}%
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 12px; border: 1px solid #ddd; font-weight: bold;">Data Points</td>
                            <td style="padding: 12px; border: 1px solid #ddd; text-align: center; font-size: 0.9em;">${data.analysis_1.sample_size} matches</td>
                            <td style="padding: 12px; border: 1px solid #ddd; text-align: center; font-size: 0.9em;">Limited</td>
                            <td style="padding: 12px; border: 1px solid #ddd; text-align: center; font-size: 0.9em;">${data.analysis_2.sample_size} matches</td>
                        </tr>
                    </tbody>
                </table>
                
                <div style="margin-top: 20px; padding: 15px; background: linear-gradient(135deg, #fff3cd 0%, #ffe8a1 100%); border-radius: 8px; border-left: 5px solid #ffc107;">
                    <strong style="font-size: 1.1em;">🎯 Best Prediction: ${data.best_prediction}</strong> @ ${data.best_odds.toFixed(2)}
                    <br><strong>Win Rate:</strong> ${data.best_win_rate.toFixed(1)}%
                    <br><strong>Upset Rate:</strong> ${data.best_upset_rate.toFixed(1)}%
                </div>
                
                <div style="margin-top: 15px; padding: 15px; background: #e8f4f8; border-radius: 8px;">
                    <strong>📝 Rationale:</strong><br/>
                    ${data.rationale}
                </div>
            </div>
        `;
        
        resultDiv.innerHTML = html;
        
    } catch (error) {
        resultDiv.innerHTML = `<div style="padding: 15px; background: #f8d7da; border-radius: 5px; color: #721c24;"><strong>Error:</strong> ${error.message}</div>`;
    }
});

// ============================================
// API UPLOAD: Handle batch screenshot uploads
// ============================================

const apiDropZone = document.getElementById('apiDropZone');

apiDropZone?.addEventListener('dragover', function(e) {
    e.preventDefault();
    apiDropZone.style.borderColor = '#0099cc';
    apiDropZone.style.backgroundColor = '#e8f4f8';
});

apiDropZone?.addEventListener('dragleave', function(e) {
    e.preventDefault();
    apiDropZone.style.borderColor = '#00d4ff';
    apiDropZone.style.backgroundColor = '';
});

apiDropZone?.addEventListener('drop', function(e) {
    e.preventDefault();
    apiDropZone.style.borderColor = '#00d4ff';
    apiDropZone.style.backgroundColor = '';
    
    const files = e.dataTransfer.files;
    document.getElementById('apiUploadFile').files = files;
    
    handleApiFileSelect(files);
});

function handleApiFileSelect(files) {
    const preview = document.getElementById('apiFilePreview');
    const container = document.getElementById('apiPreviewContainer');
    
    if (files.length === 0) {
        preview.style.display = 'none';
        return;
    }
    
    container.innerHTML = '';
    document.getElementById('apiFileName').textContent = `${files.length} file(s) selected`;
    
    Array.from(files).forEach(file => {
        const reader = new FileReader();
        reader.onload = function(e) {
            const imgWrapper = document.createElement('div');
            imgWrapper.style.cssText = 'position: relative; border-radius: 5px; overflow: hidden;';
            
            const img = document.createElement('img');
            img.src = e.target.result;
            img.style.cssText = 'width: 100%; height: 80px; object-fit: cover;';
            
            const filename = document.createElement('small');
            filename.textContent = file.name.substring(0, 12) + '...';
            filename.style.cssText = 'position: absolute; bottom: 0; left: 0; right: 0; background: rgba(0,0,0,0.7); color: white; padding: 3px; font-size: 0.7em; text-align: center;';
            
            imgWrapper.appendChild(img);
            imgWrapper.appendChild(filename);
            container.appendChild(imgWrapper);
        };
        reader.readAsDataURL(file);
    });
    
    preview.style.display = 'block';
}

function clearApiFiles() {
    document.getElementById('apiUploadFile').value = '';
    document.getElementById('apiFilePreview').style.display = 'none';
    document.getElementById('apiPreviewContainer').innerHTML = '';
    document.getElementById('apiFileName').textContent = 'Click or drag screenshots here';
}

document.getElementById('apiUploadForm')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const files = document.getElementById('apiUploadFile').files;
    if (!files || files.length === 0) {
        alert('Please select at least one screenshot');
        return;
    }
    
    const formData = new FormData();
    for (let file of files) {
        formData.append('file', file);
    }
    
    const resultDiv = document.getElementById('apiUploadResult');
    
    try {
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = `<div style="text-align: center;"><i class="fas fa-spinner loading"></i> Uploading and analyzing ${files.length} file(s)...</div>`;
        
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!data.success) {
            // Check for Tesseract OCR missing error
            if (data.tesseract_required) {
                resultDiv.innerHTML = `
                    <div style="padding: 20px; background: #fff3cd; border: 2px solid #ffc107; border-radius: 8px; color: #333;">
                        <h3 style="color: #e74c3c; margin-top: 0;">
                            <i class="fas fa-exclamation-triangle"></i> OCR Engine Not Installed
                        </h3>
                        <p style="margin: 10px 0;"><strong>Problem:</strong> Tesseract OCR engine is missing from your system.</p>
                        <p style="margin: 10px 0;"><strong>Solution:</strong> Download and install from:</p>
                        <a href="https://github.com/UB-Mannheim/tesseract/wiki/Downloads-for-Windows" 
                           target="_blank" 
                           style="display: inline-block; padding: 10px 15px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; margin: 10px 0;">
                            📥 Download Tesseract OCR for Windows
                        </a>
                        <p style="margin: 10px 0; font-size: 0.9em; color: #666;">
                            <strong>Steps:</strong><br/>
                            1. Download the installer<br/>
                            2. Run installer (as Administrator)<br/>
                            3. Complete installation<br/>
                            4. Restart this browser or Flask<br/>
                            5. Try uploading again!
                        </p>
                        <p style="margin: 10px 0; background: #e8f4f8; padding: 10px; border-radius: 5px; font-size: 0.9em;">
                            <strong>💡 Tip:</strong> Use the "API Predict" tab instead! It doesn't need OCR - just type odds like "1.8 vs 4.0"
                        </p>
                    </div>
                `;
            } else {
                resultDiv.innerHTML = `<div style="padding: 15px; background: #f8d7da; border-radius: 5px; color: #721c24;"><strong>Error:</strong> ${data.error}</div>`;
            }
            return;
        }
        
        // Build results table
        let html = `
            <div style="margin-top: 20px;">
                <h3 style="margin-bottom: 15px;">✅ Upload Results (${data.count} files processed)</h3>
        `;
        
        data.results.forEach(result => {
            const winColor = result.historical_win_rate > 55 ? '#28a745' : (result.historical_win_rate > 45 ? '#ffc107' : '#d9534f');
            const upsetColor = result.upset_rate > 30 ? '#d9534f' : '#17a2b8';
            const confColor = result.confidence >= 80 ? '#28a745' : (result.confidence >= 60 ? '#ffc107' : '#d9534f');
            
            html += `
                <div style="margin-bottom: 15px; padding: 15px; background: white; border: 2px solid #00d4ff; border-radius: 8px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <div>
                            <strong style="font-size: 1.1em;">${result.match}</strong><br/>
                            <small style="color: #666;">${result.source}</small>
                        </div>
                        <div style="background: ${result.is_favorite ? '#ffebcd' : '#e8f4f8'}; padding: 8px 12px; border-radius: 5px; font-size: 0.9em;">
                            ${result.is_favorite ? '⚡ Favorite' : '🎯 Underdog'}
                        </div>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin-bottom: 12px;">
                        <div style="padding: 10px; background: #f9f9f9; border-radius: 5px;">
                            <strong>Teams</strong><br/>
                            ${result.home_team} vs ${result.away_team}
                        </div>
                        <div style="padding: 10px; background: #f9f9f9; border-radius: 5px;">
                            <strong>Odds</strong><br/>
                            ${result.odds_display} (${result.odds_category})
                        </div>
                        <div style="padding: 10px; background: #f9f9f9; border-radius: 5px;">
                            <strong>Win %</strong><br/>
                            <span style="background: ${winColor}; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">
                                ${result.historical_win_rate.toFixed(1)}%
                            </span>
                        </div>
                        <div style="padding: 10px; background: #f9f9f9; border-radius: 5px;">
                            <strong>Upset %</strong><br/>
                            <span style="background: ${upsetColor}; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">
                                ${result.upset_rate.toFixed(1)}%
                            </span>
                        </div>
                        <div style="padding: 10px; background: #f9f9f9; border-radius: 5px;">
                            <strong>BTTS %</strong><br/>
                            ${result.btts_rate.toFixed(1)}%
                        </div>
                    </div>
                    
                    <div style="padding: 12px; background: linear-gradient(135deg, #fff3cd 0%, #ffe8a1 100%); border-radius: 5px; margin-bottom: 10px;">
                        <strong>${result.prediction}</strong> @ ${result.best_odds.toFixed(2)}<br/>
                        <small>Confidence: ${result.confidence}%</small>
                    </div>
                    
                    <div style="padding: 12px; background: #f0f9ff; border-radius: 5px; font-size: 0.95em;">
                        <strong>Rationale:</strong> ${result.rationale}
                    </div>
                </div>
            `;
        });
        
        html += `</div>`;
        
        if (data.errors && data.errors.length > 0) {
            html += `
                <div style="margin-top: 15px; padding: 12px; background: #fff3cd; border-radius: 5px;">
                    <strong>⚠️ Some files had issues:</strong>
                    <ul style="margin: 5px 0;">
                        ${data.errors.map(err => `<li>${err}</li>`).join('')}
                    </ul>
                </div>
            `;
        }
        
        resultDiv.innerHTML = html;
        
    } catch (error) {
        resultDiv.innerHTML = `<div style="padding: 15px; background: #f8d7da; border-radius: 5px; color: #721c24;"><strong>Error:</strong> ${error.message}</div>`;
    }
});

    // Handle file selection for API Upload
    document.getElementById('apiUploadFile')?.addEventListener('change', function(e) {
        handleApiFileSelect(this.files);
    });
    
    // Load stats on page load
    loadStats();
});
