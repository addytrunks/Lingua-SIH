import BeService from "./be-service";

export default class SigmlService {
  public static avatars = ["anna", "marc", "francoise", "luna", "siggi"];
  public static changeAvatar(inc: -1 | 1) {
    const menu = document.querySelector(
      "select.menuAv.av0"
    ) as HTMLSelectElement | null;
    if (!menu) return;
    const idx = this.avatars.indexOf(menu.value);
    menu.selectedIndex = (idx + inc) % this.avatars.length;
    menu.dispatchEvent(new Event("change"));
  }
  private static _getCwasa() {
    return (window as unknown as any).CWASA;
  }
  static async playSigml(text: string) {
    const words = await BeService.sigmlPreprocess(text);
    let sigmls = "";
    for (const word of words.result) {
      const res = await fetch(`/sigml/${word}.sigml`);
      const content = await res.text();
      sigmls = sigmls + content.replace("<sigml>", "").replace("</sigml>", "");
    }
    sigmls = `<sigml>${sigmls}</sigml>`;
    console.log(sigmls);

    SigmlService._getCwasa()?.playSiGMLText(sigmls);
  }
  private static _handleAvatarResize() {
    const avatar = document.querySelector(
      "div.CWASAAvatar"
    ) as HTMLDivElement | null;
    if (!avatar) return;
    const canvas = document.querySelector(
      "canvas.canvasAv"
    ) as HTMLCanvasElement | null;
    if (!canvas) return;
    canvas.width = avatar.clientWidth;
    console.log(avatar.clientHeight);

    canvas.height = avatar.clientHeight > 600 ? 600 : avatar.clientHeight;
  }
  static async initCwasa() {
    await SigmlService._getCwasa()?.init({
      jasBase: "https://vhg.cmp.uea.ac.uk/tech/jas/vhg2025/",
      avSettings: [{ initAv: "luna" }],
    });
    const avatar = document.querySelector(
      "div.CWASAAvatar"
    ) as HTMLDivElement | null;
    if (!avatar) return;
    new ResizeObserver(SigmlService._handleAvatarResize).observe(avatar);
    this._handleAvatarResize();
  }
}
