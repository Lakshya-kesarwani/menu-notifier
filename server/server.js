const express = require("express");
const cron = require("node-cron");
const axios = require("axios");
const dotenv = require("dotenv");
const menu = require("./menu");

dotenv.config();
const app = express();
const PORT = process.env.PORT || 3000;
const PUSHBULLET_TOKEN = process.env.PUSHBULLET_TOKEN;

function sendPush(title, body) {
  axios.post(
    "https://api.pushbullet.com/v2/pushes",
    {
      type: "note",
      title: title,
      body: body
    },
    {
      headers: {
        "Access-Token": PUSHBULLET_TOKEN,
        "Content-Type": "application/json"
      }
    }
  ).then(res => {
    console.log(`[${title}] Sent: ${res.status}`);
  }).catch(err => {
    console.error("Pushbullet Error:", err.response?.data || err.message);
  });
}

function formatMeal(day, meal) {
  const dayMenu = menu[day.toLowerCase()];
  if (!dayMenu || !dayMenu[meal.toLowerCase()]) {
    return `No menu available for ${meal} on ${day}`;
  }
  return dayMenu[meal.toLowerCase()];
}

function notifyMeal(meal) {
  const today = new Date().toLocaleString("en-US", { weekday: "long" }).toLowerCase();
  const title = `🍽️ ${meal} Reminder - ${today}`;
  const body = formatMeal(today, meal);
  sendPush(title, body);
}

// ⏰ Schedule notifications
cron.schedule("15 7 * * 1-5", () => notifyMeal("Breakfast")); // Mon-Fri 7:15
cron.schedule("45 7 * * 6,0", () => notifyMeal("Breakfast")); // Sat-Sun 7:45
cron.schedule("10 12 * * *", () => notifyMeal("Lunch"));      // Daily 12:10
cron.schedule("0 16 * * *", () => notifyMeal("Snacks"));      // Daily 16:00
cron.schedule("43 22 * * *", () => notifyMeal("Dinner"));     // Daily 19:41

// 🏠 Route
app.get("/", (req, res) => {
  res.send("Server is running");
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
