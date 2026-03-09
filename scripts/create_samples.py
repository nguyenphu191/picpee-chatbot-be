import os
from fpdf import FPDF

output_dir = "test_docs"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def create_pdf(filename, title, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    # Tương thích FPDF cũ và mới
    try:
        pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT", align='C')
    except TypeError:
        pdf.cell(0, 10, title, ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(0, 10, content)
    
    file_path = os.path.join(output_dir, filename)
    pdf.output(file_path)
    print(f"✅ Created: {file_path}")

# ==========================================
# 1. User Guide - PicPee (English format)
# ==========================================
doc1_title = "User Guide - PicPee AI Editor"
doc1_content = """I. Introduction to PicPee
Welcome to the comprehensive user guide for PicPee, the next-generation cloud-based photo editing platform. PicPee is engineered to bridge the gap between complex professional desktop software and oversimplified mobile editing apps. By utilizing advanced machine learning algorithms and a highly optimized WebGL rendering engine, PicPee provides instantaneous feedback and high-fidelity output right in your browser, without requiring any heavy installations. Whether you are a professional photographer looking to quickly batch process a wedding shoot, a social media influencer aiming for perfectly curated feeds, or a small business owner creating e-commerce product listings, PicPee provides the exact tools you need in an intuitive, accessible interface.

II. Getting Started and Workspace Overview
1. Account Registration and Login
To begin using the full capabilities of PicPee, head over to the sign-up page. You can register using your Google or Apple credentials for single sign-on convenience, or you can opt for a traditional email and password combination. Upon initial login, you will be greeted by the Dashboard, which serves as your central hub.

2. The Dashboard Interface
The Dashboard is divided into three primary sections: the Project Gallery, the Asset Library, and the Quick Actions panel. The Project Gallery displays all your historical edits, automatically synced to the cloud. The Asset Library allows you to upload and organize raw images, logos, and watermarks. The Quick Actions panel provides one-click shortcuts to our most popular features, such as "Remove Background" or "Apply Vintage Filter".

III. Core Editing Features in Detail
a. AI-Powered Background Removal
Our flagship feature is the Neural Edge Detection background removal tool. Unlike traditional magic wand tools that require tedious manual selection and refinement, our AI analyzes the semantic structure of the image. It distinguishes between foreground subjects (people, animals, cars, products) and background elements with near-perfect accuracy, even handling complex areas like wispy hair, transparent glass, and fur. 
To use this feature, simply click the "Remove BG" button while an image is selected. The process takes entirely on our secure cloud servers and typically returns a perfectly masked PNG within 0.8 seconds. You can then choose to leave the background transparent, fill it with a solid color, or replace it from our library of high-resolution stock backgrounds.

b. Advanced Color Grading and Cinematic Filters
PicPee goes beyond basic brightness and contrast sliders. We offer professional-grade color wheels for midtones, highlights, and shadows, allowing for precise cinematic color grading. Furthermore, our Filter Library boasts over 150 meticulously crafted presets. These are categorized into themes such as 'Golden Hour', 'Cyberpunk', 'Film Emulation', and 'Monochrome'. Premium users have the added ability to create, save, and export their own custom filter presets, ensuring a consistent visual identity across all their brand materials.

c. Intelligent Object Removal (Magic Eraser)
Have a perfect landscape shot ruined by a stray power line, or a great portrait with an unwanted photobomber? The Magic Eraser tool utilizes generative content-aware fill to remove these imperfections seamlessly. Select the brush tool, highlight the unwanted object, and the AI will analyze the surrounding pixels and underlying textures to reconstruct the area as if the object was never there. This feature works exceptionally well on continuous textures like sky, grass, brick walls, and water.

IV. Exporting and Sharing
1. Supported Formats and Resolutions
PicPee supports importing a wide variety of formats including JPEG, PNG, WEBP, HEIC, and RAW files from major camera manufacturers (Sony, Canon, Nikon). When exporting, you can choose to save your masterpiece as a highly compressed JPEG for web use, a lossless PNG to preserve transparency, or a modern WEBP for optimal balance of quality and file size. Free users can export up to 1080p resolution, while Premium subscribers enjoy unrestricted 4K and native resolution exports.

2. Direct Social Media Integration
Save time by publishing directly from the PicPee editor. You can link your Instagram, Twitter, and Facebook accounts to push your edited images directly to your feed or stories, complete with auto-sizing options customized for each platform's specific dimensional requirements."""

# ==========================================
# 2. Frequently Asked Questions (FAQ)
# ==========================================
doc2_title = "Frequently Asked Questions (FAQ)"
doc2_content = """I. Subscription and Billing Inquiries
1. What are the differences between the Free, Pro, and Enterprise plans?
The Free plan is designed for casual users and includes access to all basic editing tools, 15 standard filters, and up to 30 exports per day at a maximum resolution of 1080p. AI features like Background Removal are limited to 5 uses daily. 
The Pro plan, billed at $9.99/month, unlocks the full potential of PicPee. It includes unlimited 4K exports, access to the entire library of 150+ premium filters, unlimited AI Background Removal, Magic Eraser usage, and batch processing capabilities. Pro users also get 100GB of secure cloud storage.
The Enterprise plan is tailored for agencies and large teams. It includes everything in Pro, plus centralized team billing, collaborative workspaces, custom font uploads, dedicated API access for integration into internal workflows, and a 99.9% uptime SLA.

2. Can I cancel my subscription at any time? Will I get a refund?
Yes, you can cancel your Premium or Enterprise subscription at any point directly from your Account Settings page under the 'Billing' tab. Your premium features will remain active until the end of your current billing cycle (monthly or annual). Because you retain access until the cycle concludes, we do not issue prorated refunds for partially used billing periods, except where required by specific local consumer protection laws.

3. Do you offer student or educator discounts?
Absolutely. We support the creative community and educational institutions. Students and teachers with a verifiable .edu email address or equivalent institution ID are eligible for a 50% discount on the Pro plan. Please visit the 'Education' section in our footer and fill out the verification form. Verification is handled by a third-party partner and is usually approved within 15 minutes.

II. Technical Support and Troubleshooting
a. The web editor is freezing or running very slowly on my computer. How can I fix this?
PicPee relies heavily on WebGL and your computer's GPU to render effects in real-time. If you are experiencing performance issues, the most common culprit is that hardware acceleration is disabled in your browser settings. 
In Google Chrome, navigate to Settings > System and ensure "Use hardware acceleration when available" is toggled on. In Safari, it is enabled by default. Firefox users should check Settings > General > Performance. 
If hardware acceleration is enabled and you still face issues, ensure your graphics drivers are up to date. Additionally, very large RAW files (over 50MB) may take longer to initialize, depending on your system's RAM limit. We recommend having at least 8GB of system RAM for a smooth experience when handling high-resolution assets.

b. My exported images look blurry or compressed compared to the editor view. Why?
There are two potential reasons for this. Firstly, if you are a Free tier user, your exports are capped at 1080p on the longest edge. If you upload a 4K image, it will be downscaled upon export, which can result in a perceived loss of sharpness on large, high-DPI displays. 
Secondly, check your export settings dialogue box. If you are exporting as a JPEG, ensure the quality slider is set to at least 85% for high-quality web use, or 100% for maximum fidelity. If you are dealing with sharp graphics, text, or transparent elements, always choose the PNG export format, as JPEG compression artifacts can make sharp edges appear blurry.

III. Feature Requests and Beta Program
1. I have an idea for a new feature. How can I submit it?
We love hearing from our community! You can submit feature requests, suggest improvements, or vote on existing ideas by navigating to our public roadmap via the 'Feedback' link located in your user profile drop-down menu. Our product engineering team reviews these submissions weekly, and the most upvoted features are prioritized for upcoming development sprints.

2. How do I join the Early Access / Beta testing program?
We occasionally invite active users to test experimental features before they are rolled out to the general public. To express your interest, go to Account Settings > Preferences and toggle 'Opt-in to Beta testing'. Please note that Beta features may be instable and could cause unexpected browser crashes; we advise against using Beta builds for critical, time-sensitive client work."""

# ==========================================
# 3. Privacy Policy
# ==========================================
doc3_title = "Privacy & Security Policy"
doc3_content = """I. Comprehensive Data Processing and Storage
1. Uploaded Image Data Handling
Your privacy and the security of your creative assets are our highest priorities. When you upload an image to PicPee for editing, the file is transmitted via an encrypted connection to our secure cloud servers hosted by Amazon Web Services (AWS) in the United States and the European Union. 
For users without an account, or Free tier users who do not explicitly save their projects to the cloud, all uploaded images and their edited derivatives are considered ephemeral. They are held temporarily in volatile server memory solely for the duration of your active editing session. If your session is inactive for 24 hours, these files are systematically and permanently wiped from our systems by automated garbage collection scripts. We maintain absolutely no backups or hidden archives of these ephemeral files.

2. Cloud Storage for Registered Users
For registered Pro and Enterprise users who utilize our Cloud Storage feature, your images, project files, and custom presets are stored persistently on encrypted SSD volumes. This allows you to close your browser and resume your edits days or weeks later from any device. You maintain full ownership and copyright of all materials uploaded. You can delete specific projects or your entire library at any time. When a deletion request is initiated by a user, a hard delete command is executed across all primary and redundant database nodes instantly.

II. Personal Information Collection and Usage Practices
a. Account Information
To provide the PicPee service, we must collect basic account information during the registration process. This includes your email address (used as your primary login identifier and for critical service-related communications), a hashed and salted representation of your password (we never store plain-text passwords), and your billing information if you subscribe to a premium tier. All payment processing is handled securely off-site by Stripe PCI-DSS Level 1 compliant infrastructure; PicPee servers never process or touch your full credit card numbers.

b. Usage Analytics and Telemetry
To continuously improve the performance and usability of our editor, we collect anonymized telemetry data. This includes non-identifying metrics such as average session duration, the frequency of specific tool usage (e.g., how often the 'Vintage' filter is applied), browser type, and general geographic location (at the city/country level, mask-aggregated). We use this data strictly for internal product development and load-balancing optimization. 
We definitively state that PicPee does NOT sell, rent, or lease any user data - whether personal identifying information or anonymized telemetry - to third-party advertising networks, data brokers, or marketing agencies under any circumstances.

III. Cookies, Tracking, and Third-Party Integrations
1. Essential and Functional Cookies
PicPee utilizes cookies (small text files stored within your browser) to ensure the core functionality of the application. These "Essential Cookies" are required to maintain your active login session, remember your UI theme preference (Dark/Light mode), and load your custom workspace layouts. The service cannot function properly without these cookies.

2. Integration with External Platforms
If you choose to use our "Direct Export" features to publish your edits straight to social media networks like Facebook or Twitter, we must authenticate with those services using OAuth tokens. We only request the minimum permissions necessary to post the image on your behalf. We do not read your timelines, access your private messages, or scrape your friend lists. The OAuth tokens are stored securely and can be revoked by you at any time either from your PicPee settings or directly from the respective social network's security panel."""

if __name__ == "__main__":
    create_pdf("user_guide_en.pdf", doc1_title, doc1_content)
    create_pdf("faq_en.pdf", doc2_title, doc2_content)
    create_pdf("privacy_policy_en.pdf", doc3_title, doc3_content)
    print("\n🚀 All 3 English PDFs generated inside 'test_docs' directory!")

