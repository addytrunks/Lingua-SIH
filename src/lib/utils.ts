export function base64ToArrayBuffer(base64: string) {
  var binaryString = atob(base64);
  var bytes = new Uint8Array(binaryString.length);
  for (var i = 0; i < binaryString.length; i++) {
    bytes[i] = binaryString.charCodeAt(i);
  }
  return bytes.buffer;
}
export function base64TUrl(data: string) {
  let bytes = base64ToArrayBuffer(data);
  const blob = new Blob([bytes], { type: "audio/mp3" });
  return window.URL.createObjectURL(blob);
}
