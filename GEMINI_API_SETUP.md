# 🔷 How to Get Your Gemini API Key

## Quick Steps (5 minutes)

### 1. Visit Google AI Studio
Go to: **https://makersuite.google.com/app/apikey**

### 2. Sign In
- Use your Google account
- Accept terms and conditions

### 3. Create API Key
- Click **"Get API Key"** button
- Click **"Create API key in new project"**
- Copy the generated key immediately

### 4. Use in OmniCare AI

**Option A: Enter in App (Easy)**
1. Open OmniCare AI in your browser
2. Look for the sidebar on the right
3. Find "🔷 Gemini API Key (Optional)" field
4. Paste your API key
5. Start using enhanced features!

**Option B: Environment Variable (Recommended for developers)**
1. Create a `.env` file in project root (copy from `.env.example`)
2. Add your key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```
3. Save the file
4. Restart the app

## What You Get With Gemini

### 📚 Education Tutor
- **AI-powered explanations** adapted to your level
- **Custom examples** for any topic
- **Practice problems** generated on demand
- **Interactive learning** with follow-up questions

### 🏥 Healthcare Navigator
- **Detailed health information** (educational only)
- **Comprehensive symptom explanations**
- **Prevention and wellness tips**
- **Medical terminology simplified**

## Important Notes

⚠️ **Keep Your Key Safe:**
- Never share your API key publicly
- Don't commit it to Git
- The `.env` file is already in `.gitignore`

💰 **Gemini Pricing:**
- **Free tier**: 60 requests per minute
- More than enough for personal use
- No credit card required for free tier

🔒 **Privacy:**
- Your API key stays on your device
- Not stored on any server
- You control all API calls

## Troubleshooting

**Error: "GEMINI_API_KEY not found"**
- Make sure you entered the key in the sidebar
- Or check your `.env` file exists and has the correct format

**Error: "API quota exceeded"**
- Wait a minute and try again
- Free tier has 60 requests/minute limit

**Error: "Invalid API key"**
- Double-check you copied the entire key
- Make sure there are no extra spaces
- Try generating a new key

## Need Help?

Visit: https://ai.google.dev/docs
