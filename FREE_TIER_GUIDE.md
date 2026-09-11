# Free Tier Guide - Build This Without Spending Money

This guide shows you how to set up and run the entire automation tool using **100% free services**.

## Free API Services

### 1. OpenAI - Free Trial ($5 credit)

**What you get:**
- $5 free credits (usually lasts ~2-4 weeks)
- Access to GPT-4o, GPT-3.5-turbo
- Enough for 50+ videos at starter level

**How to get it:**
1. Go to https://platform.openai.com/signup
2. Sign up with email or Google
3. Add phone number (for verification)
4. Verify email
5. You'll get $5 free credit automatically
6. API key is on: https://platform.openai.com/account/api-keys

**Cost breakdown:**
- GPT-4o: ~$0.03 per 1K input tokens, $0.06 per 1K output tokens
- For a 5-minute video script: ~$0.10-0.30 per video
- Your $5 credit = ~15-50 videos depending on script length

**Tips to maximize:**
```yaml
# In config.yaml - use cheaper model for prototyping
openai:
  model: "gpt-3.5-turbo"  # Much cheaper than gpt-4o
  temperature: 0.7
  max_tokens: 1500        # Reduce to save tokens
```

---

### 2. ElevenLabs - Free Tier (10,000 characters/month)

**What you get:**
- 10,000 characters per month FREE
- Access to 15+ voices
- Good quality TTS

**Character counting:**
- Average script: 500-1000 characters
- 10,000 characters = ~10-20 videos/month FREE
- After free tier: $5-15/month for more characters

**How to get it:**
1. Go to https://elevenlabs.io
2. Sign up (no credit card required!)
3. Go to Account → API Key (copy it)
4. Go to Voice Library → Select any voice (copy Voice ID)
5. Done!

**Monitor your usage:**
```bash
# Check your character count
python3 << 'EOF'
import os
import requests
from dotenv import load_dotenv

load_dotenv()
key = os.getenv('ELEVENLABS_API_KEY')
headers = {'xi-api-key': key}
response = requests.get('https://api.elevenlabs.io/v1/user', headers=headers)
data = response.json()
print(f"Character balance: {data.get('character_count', 0):,} / 10,000")
EOF
```

---

### 3. YouTube Videos - Free to Download

**Getting source material:**
- Use any public YouTube video
- yt-dlp automatically handles downloading
- No API key needed!
- No cost!

**Recommended sources:**
- Music videos (react to music)
- Trending clips
- Fail compilations
- Gaming moments
- Internet lore deep dives

---

## Free AI Tools for Sprite Generation

### Option 1: Bing Image Creator (FREE)

```
1. Go to https://www.bing.com/images/create
2. Sign in with Microsoft account (free)
3. Prompt: "cute anime character with wolf ears, transparent background, PNG"
4. Generate 7 different variations
5. Download PNG files
6. Place in assets/sprites/
```

**Advantages:**
- 100% free
- No watermarks
- Good quality
- Fast generation

### Option 2: Leonardo.AI (FREE)

```
1. Go to https://leonardo.ai
2. Sign up (free account)
3. Use "Image Generation" tab
4. Prompt examples:
   - "happy anime character, transparent bg"
   - "cool cat character with sunglasses"
   - "space wolf with glowing eyes"
5. Download PNGs
```

**Advantages:**
- Free tier: 150 credits/day
- Each generation: 8-32 credits
- Can generate 5-10 images daily

### Option 3: Stable Diffusion Web (100% FREE)

```
1. Go to https://huggingface.co/spaces/stabilityai/stable-diffusion-2
2. No account needed
3. Type prompt
4. Generate immediately
5. Download results
```

**Advantages:**
- Completely free
- No login needed
- No watermarks
- Unlimited generations

### Option 4: OpenAI DALL-E Mini (MAGE.SPACE)

```
1. Go to https://www.mage.space/
2. Type prompt
3. Generate (free credits daily)
4. Download
```

---

## Budget Breakdown - $0

| Item | Cost | Free Alternative |
|------|------|------------------|
| **OpenAI API** | $5-50/mo | $5 free trial → use GPT-3.5-turbo |
| **ElevenLabs** | $5-99/mo | 10,000 chars/month free tier |
| **Video Host** | $0 | YouTube (post directly) |
| **Sprite Generator** | $0 | Bing/Leonardo/Stable Diffusion |
| **Python** | $0 | Free |
| **FFmpeg** | $0 | Free |
| **Git/GitHub** | $0 | Free |
| **Editor** | $0 | VS Code (free) |
| **TOTAL** | **$0** | **$0 (then $5 trial credit)** |

---

## Cost Optimization Tips

### Tip 1: Use Cheaper Models

```yaml
# Original (expensive)
openai:
  model: "gpt-4o"          # $0.03-0.06 per 1K tokens
  max_tokens: 2000

# Budget-friendly
openai:
  model: "gpt-3.5-turbo"   # $0.0005-0.0015 per 1K tokens
  max_tokens: 1500         # Shorter scripts
```

**Savings**: 50x cheaper per video!

### Tip 2: Batch Processing

```bash
# Generate 10 scripts in bulk
python3 batch_processor.py --topics "breakcore,gaming,weird-lore" --output scripts.json
```

### Tip 3: Monitor Spending

```bash
python3 monitor_costs.py
```

---

## Summary

✅ **Setup Cost: $0**
✅ **Monthly Cost: $0** (using free tiers)
✅ **Equipment: Just a computer**
✅ **Time to first video: 30 minutes**

Everything you need is FREE!
