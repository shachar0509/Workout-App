# Google sign-in and cloud sync: one-time Firebase setup

The app works as a guest (data on the device) without any setup. To enable "Continue with Google"
and cloud sync, create a free Firebase project once and paste its web config into `app.html`.

1. Open https://console.firebase.google.com, **Add project** (the free Spark plan is enough; no credit card).
2. **Build > Authentication > Get started > Sign-in method > Google > Enable**.
3. **Authentication > Settings > Authorized domains > Add domain**: `shachar0509.github.io`
   (use the domain your GitHub Pages site is served from).
4. **Build > Firestore Database > Create database** (production mode, a region near you).
5. **Firestore > Rules**, replace with the following and **Publish** (each user can read and write only their own data):

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{uid}/{document=**} {
      allow read, write: if request.auth != null && request.auth.uid == uid;
    }
  }
}
```

6. **Project settings > General > Your apps > Web app (</>)**: register an app and copy `firebaseConfig`.
7. In `app.html`, fill in `FB_CONFIG` (search for `var FB_CONFIG`) with `apiKey`, `authDomain`, `projectId` and `appId`, then commit and push.

The web `apiKey` is not a secret: access is protected by the rules above.

Data layout in Firestore: `users/{uid}/workouts`, `users/{uid}/templates`, `users/{uid}/exercises`, `users/{uid}/settings/app`.
