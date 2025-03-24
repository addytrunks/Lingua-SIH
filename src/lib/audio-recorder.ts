import MediaStreamRecorder from "msr";

export default class AudioRecorder {
  private _msr: MediaStreamRecorder;
  private _stream: MediaStream;
  private _chunks: Blob[] = [];
  private _onAudioRecordingStopped: (audio: string) => void;

  private _blobToBase64(blob: Blob) {
    return new Promise<string>((resolve, _) => {
      const reader = new FileReader();
      reader.onloadend = () => {
        resolve((reader.result as string).split(",")[1]);
      };
      reader.readAsDataURL(blob);
    });
  }
  constructor(
    mediaStream: MediaStream,
    onAudioRecordingStopped: (blob: string) => void
  ) {
    this._stream = mediaStream;
    this._onAudioRecordingStopped = onAudioRecordingStopped;
    this._msr = new MediaStreamRecorder(this._stream);
    this._msr.mimeType = "audio/wav";
    this._msr.ondataavailable = (blob: Blob) => {
      this._chunks.push(blob);
    };
    // const msrStop = this._msr.stop;
    // this._msr.stop = () => {
    //   msrStop();
    //   const blob = new Blob(this._chunks, { type: "audio/wav" });
    //   this._blobToBase64(blob).then((audio) => {
    //     this._onAudioRecordingStopped(audio);
    //   });
    // };
  }

  startRecording() {
    this._msr.start(10000);
  }

  stopRecording() {
    this._msr.stop();
    console.log(this._chunks);

    const blob = new Blob(this._chunks, { type: "audio/wav" });
    this._chunks = [];
    this._blobToBase64(blob).then((audio) => {
      this._onAudioRecordingStopped(audio);
    });
  }
}
