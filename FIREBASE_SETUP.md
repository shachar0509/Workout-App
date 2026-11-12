# Google sign-in and cloud sync: one-time Firebase setup

The app works as a guest (data on the device) without any setup. To enable "Continue with Google"
and cloud sync, create a free Firebase project once and give its web config to the app.

**This repository is public: never commit the config (or any key) to it.** The app keeps the config on each
device (browser storage) and never reads it from the repository.

1. Open https://console.firebase.google.com, **Add project** (the free Spark plan is enough; no credit card).
2. **Build > Authentication > Get started > Sign-in method > Google > Enable**.
3. **Authentication > Settings > Authorized domains > Add domain**: `<your-username>.github.io`
   (the domain your GitHub Pages site is served from).
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
7. Give the config to the app, on each device, in one of two ways:
   - Open the app, **Continue with Google > Google connection setup**, paste the `firebaseConfig` block and tap **Save config**
     (or, as a guest, the same box under **Settings > Account**).
   - Or open a private setup link of the form `https://<your-username>.github.io/<repo>/#fb=...`. Signed in on one device,
     **Settings > Account > Copy setup link** creates it. Send it only to people you trust (WhatsApp, not a public post):
     it contains the web config.

The web `apiKey` is not a password: access to the data is protected by the rules above. It is still kept out of the repository.

Data layout in Firestore: `users/{uid}/workouts`, `users/{uid}/templates`, `users/{uid}/exercises`, `users/{uid}/settings/app`.
