// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
// import { getAnalytics } from "firebase/analytics";
import { getAuth } from "firebase/auth";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: process.env.REACT_APP_FIREBASE_API_KEY,
  authDomain: process.env.REACT_APP_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID,
  storageBucket: process.env.REACT_APP_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.REACT_APP_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.REACT_APP_FIREBASE_APP_ID,
  measurementId: process.env.REACT_APP_FIREBASE_MEASUREMENT_ID,
};

console.log(firebaseConfig);

// Initialize Firebase
// Basic runtime validation to catch missing env vars early and provide a clearer error
const requiredKeys = [
  "apiKey",
  "authDomain",
  "projectId",
  "appId",
];
const missing = requiredKeys.filter((k) => !firebaseConfig[k]);
if (missing.length > 0) {
  console.error("Firebase configuration is missing required keys:", missing, firebaseConfig);
  // throw an informative error so it's obvious during development
  throw new Error(
    `Firebase configuration missing required keys: ${missing.join(", ")}. ` +
      `Make sure your interface/.env contains REACT_APP_FIREBASE_* vars and restart the dev server.`
  );
}

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Export the Firebase services you'll use
export { auth, app };
