# menu-notifier

A simple Python app to send daily mess meal notifications to your phone using Pushbullet.

## Setup Instructions

1. **Install Pushbullet on your phone**
   - Download the Pushbullet app from the [Google Play Store](https://play.google.com/store/apps/details?id=com.pushbullet.android) or [Apple App Store](https://apps.apple.com/app/pushbullet/id810352052).

2. **Sign up on the Pushbullet app**
   - Create an account or sign in using your Google or Facebook credentials.

3. **Get your Pushbullet Access Token**
   - Go to [www.pushbullet.com](https://www.pushbullet.com) and sign in with the same account.
   - Click on your profile picture > **Settings** > **Create Access Token**.
   - Copy the generated token.

4. **Clone this project**
   ```sh
   git clone <repository-url>
   cd menu-notifier
   ```

5. **Create a `.env` file**
   - In the project root, create a file named `.env`.

6. **Add your Pushbullet token to `.env`**
   ```
   PUSHBULLET_TOKEN=your_access_token_here
   ```

7. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

8. **Run the app**
   ```sh
   python api/index.py
   ```

## How it works

As long as the app is running, it will send timely mess meal notifications to your phone via Pushbullet.