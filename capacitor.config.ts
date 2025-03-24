import type { CapacitorConfig } from "@capacitor/cli";

const config: CapacitorConfig = {
  appId: "com.example.lingua",
  appName: "Lingua",
  webDir: "build",
  bundledWebRuntime: false,
  server: {
    hostname: "localhost",
    cleartext: true,
    androidScheme: "http",
    allowNavigation: [
      "http://172.16.214.35:5000/*",
      "http://192.168.7.44:5000/*",
      "http://192.168.7.44:5050/*",
      "http://192.168.7.44:5500/*",
      "http://172.16.44.60:5000/*",
      "http://172.16.44.60:5050/*",
      "http://172.16.44.60:5500/*",
    ],
  },
};

export default config;
