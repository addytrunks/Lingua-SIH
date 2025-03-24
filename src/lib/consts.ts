export class ServerHelper {
  static ip = localStorage.getItem("app-sip");
  static translateBaseURL = `http://${this.ip}:5500`;
  static mainBaseURL = `http://${this.ip}:5000`;
  static t2iBaseURL = `http://${this.ip}:5050`;
}
