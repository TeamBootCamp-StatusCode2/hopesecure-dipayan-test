# 🚀 Multi-Domain Phishing Campaign - Demo & Usage Guide

## ভাই, দেখো কোথায় আছে Multi-Domain Campaign Option! 

### 📍 **Dashboard এ Multi-Domain Campaign Card:**

Dashboard এ login করার পর আপনি একটা **নীল রঙের special card** দেখতে পাবেন:

```
🌐 Multi-Domain Campaign [NEW]
Multiple domain extensions দিয়ে advanced phishing
```

এই card এ click করলেই `/campaign/multi-domain` page এ যাবেন।

---

## 🎯 **Multi-Domain Campaign Features:**

### 1. **Domain Type Selection:**
- **Corporate** (Microsoft, Google spoofing)
- **Banking** (Bank fraud alerts)  
- **Social Media** (Facebook, Twitter spoofing)
- **E-commerce** (Amazon delivery notifications)
- **Government** (Official notices)

### 2. **Email Template Options:**
- **Microsoft Security Alert** - `security@microsoft-update.com`
- **Google Account Verification** - `noreply@google-security.net`
- **Bank Fraud Alert** - `fraud@bank-verification.org`

### 3. **Advanced Configuration:**
- ✅ Random domain rotation
- ✅ Email delay (rate limiting)
- ✅ Target email management
- ✅ Test email functionality
- ✅ Real-time campaign monitoring

---

## 📧 **Email Examples যা পাঠানো হবে:**

### Microsoft Security Alert:
```
From: security@microsoft-update.com
Subject: 🔒 Microsoft Security Alert - Immediate Action Required

Dear John,
We detected unusual activity in your Microsoft account.
⚠️ Immediate action required to secure your account

[Verify Account Security] → Click tracking URL
```

### Google Verification:
```
From: noreply@google-security.net  
Subject: 🔐 Google Account Verification Required

Hello John,
Your Google account requires immediate verification.
🚨 Account will be suspended in 24 hours

[Verify Now] → Click tracking URL
```

### Bank Fraud Alert:
```
From: fraud@bank-verification.org
Subject: 🏦 URGENT: Suspicious Activity Detected

Dear John,
Suspicious transactions detected:
• $500.00 - Online Purchase
• $1,200.00 - ATM Withdrawal

[Verify Transactions] → Click tracking URL
```

---

## 🔧 **কিভাবে ব্যবহার করবেন:**

### Step 1: Dashboard থেকে Access
1. Dashboard এ login করুন
2. **"🌐 Multi-Domain Campaign [NEW]"** card এ click করুন
3. Multi-domain campaign page open হবে

### Step 2: Campaign Configure করুন
```typescript
Campaign Name: "Q1 Security Assessment 2025"
Domain Type: Corporate  
Email Template: Microsoft Security Alert
Random Domains: ✅ Enabled
Email Delay: 2 seconds
```

### Step 3: Target Emails Add করুন
```
bolbonakano@gmail.com
test@company.com  
user@organization.org
```

### Step 4: Test Email পাঠান
- **"Send Test Email"** button click করুন
- First target email এ test পাঠাবে
- Success message দেখবেন

### Step 5: Full Campaign Launch করুন
- **"Launch Campaign"** button click করুন
- All target emails এ campaign পাঠাবে
- Real-time results দেখতে পাবেন

---

## 📊 **Campaign Results Example:**

```json
Campaign Results:
✅ Sent: 245 emails
❌ Failed: 5 emails  
📧 Total: 250 emails

Emails Sent Details:
• user1@company.com ← security@microsoft-update.com (Microsoft Security)
• user2@company.com ← noreply@google-security.net (Google Verification)  
• user3@company.com ← fraud@bank-verification.org (Bank Alert)

Domain Statistics:
• microsoft-update.com: 85.5% success rate
• google-security.net: 92.1% success rate
• bank-verification.org: 78.3% success rate
```

---

## 🌐 **Available Domains:**

### Verified Domains (যা ব্যবহার করতে পারবেন):
```
✅ microsoft-update.com (Corporate spoofing)
✅ google-security.net (Google alerts)
✅ bank-verification.org (Banking alerts)
✅ facebook-security.info (Social media)
✅ amazon-delivery.co (E-commerce)
✅ gov-notice.org (Government notices)
```

### Email Addresses Generated:
```
security@microsoft-update.com
notifications@microsoft-update.com
admin@microsoft-update.com
support@microsoft-update.com

noreply@google-security.net
alerts@google-security.net  
verification@google-security.net

fraud@bank-verification.org
alerts@bank-verification.org
security@bank-verification.org
```

---

## 🚀 **Advanced Features:**

### 1. **Random Domain Rotation:**
- প্রতিটি email আলাদা domain থেকে পাঠানো হয়
- Spam detection avoid করে
- More realistic campaigns

### 2. **Click Tracking:**
- Unique tracking URL প্রতিটি email এর জন্য
- Real-time click monitoring  
- Detailed analytics

### 3. **Rate Limiting:**
- Configurable delay between emails
- SendGrid API compliance
- Avoid rate limiting issues

### 4. **Template Personalization:**
- Recipient name automatically inserted
- Professional email formatting
- Realistic company branding

---

## 🎉 **Summary:**

**এই Multi-Domain System দিয়ে আপনি পারবেন:**

✅ **Professional phishing campaigns** চালাতে  
✅ **Multiple domain extensions** ব্যবহার করতে  
✅ **Realistic email spoofing** করতে  
✅ **Advanced tracking ও analytics** পেতে  
✅ **SendGrid integration** এর মাধ্যমে reliable delivery পেতে  

**Perfect for cybersecurity awareness training এবং penetration testing!** 🔥

---

## 📱 **Quick Access:**

### Dashboard Card Location:
```
Dashboard → Quick Actions Section → 
"🌐 Multi-Domain Campaign [NEW]" (নীল রঙের card)
```

### Direct URL:
```
http://localhost:8080/campaign/multi-domain
```

### Backend API Endpoints:
```
POST /api/campaigns/multi-domain/create/
GET /api/campaigns/multi-domain/domains/
POST /api/campaigns/multi-domain/test-email/
GET /api/campaigns/multi-domain/statistics/
```

**এখন আর confusion নাই! Multi-Domain Campaign সব ready! 🚀**
