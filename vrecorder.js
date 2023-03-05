////const getmiceacesses = function () {
////const stream = navigator.mediaDevices
////.getUserMedia({ audio: true })
////.then(function (stream) {const mediaRecorder = new MediaRecorder(stream);
////  const audioChunks = [];
////
////  mediaRecorder.addEventListener("dataavailable", (event) => {
////    audioChunks.push(event.data);
////  });
////});};
////
////const recording = document.querySelector(`.recorder`);
////recording.addEventListener(`click`, getmiceacesses);
//
//        function playAudio(audioChunks) {
//          const blob = new Blob(audioChunks,{type:'audio/x-mpeg-3'});
//          const audioPlayer = document.getElementById('audioPlayer')
//          audioPlayer.src = URL.createObjectURL(blob);
//          audioPlayer.controls=true;
//          audioPlayer.autoplay=true;
//        }
//
//       var mediaRecorder; // Need to be accessible for the stopRecorder function
//       const audioChunks = []; // Place it here to debug it contents after finsih recording
//
//        const getmiceacesses = function () {
//        const stream = navigator.mediaDevices.getUserMedia({ audio: true })
//        .then(function (stream) {
//            mediaRecorder = new MediaRecorder(stream);
//
//             mediaRecorder.start();
//
//             setTimeout(stopRecorder, 10000) // To automatically stop the recorder after 10 seconds
//
//            mediaRecorder.addEventListener("dataavailable", (event) => {
//                audioChunks.push(event.data);
//                playAudio(audioChunks)
//                console.log('Debugging Breakpoint')
//            });
//        })
//      ;};
//
//
//     const stopRecorder = function(){
//         if(mediaRecorder.state === 'recording'){
//            mediaRecorder.stop();
//         }
//     }
//
//     const recording = document.querySelector('.recorder');
//     recording.addEventListener('click', getmiceacesses);
//
//     const stopRecording = document.querySelector('.stopRecorder');
//     stopRecording.addEventListener('click', stopRecorder);
navigator.mediaDevices.getUserMedia({ audio: true })
  .then(stream => {
    const mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.start();
  });

  navigator.mediaDevices.getUserMedia({ audio: true })
  .then(stream => {
    const mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.start();

    const audioChunks = [];

    mediaRecorder.addEventListener("dataavailable", event => {
      audioChunks.push(event.data);
    });
  });

  navigator.mediaDevices.getUserMedia({ audio: true })
  .then(stream => {
    const mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.start();

    const audioChunks = [];

    mediaRecorder.addEventListener("dataavailable", event => {
      audioChunks.push(event.data);
    });

    setTimeout(() => {
      mediaRecorder.stop();
    }, 3000);
  });

  navigator.mediaDevices.getUserMedia({ audio: true })
  .then(stream => {
    const mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.start();

    const audioChunks = [];
    mediaRecorder.addEventListener("dataavailable", event => {
      audioChunks.push(event.data);
    });

    mediaRecorder.addEventListener("stop", () => {
      const audioBlob = new Blob(audioChunks);
    });

    setTimeout(() => {
      mediaRecorder.stop();
    }, 3000);
  });

  navigator.mediaDevices.getUserMedia({ audio: true })
  .then(stream => {
    const mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.start();

    const audioChunks = [];
    mediaRecorder.addEventListener("dataavailable", event => {
      audioChunks.push(event.data);
    });

    mediaRecorder.addEventListener("stop", () => {
      const audioBlob = new Blob(audioChunks);
      const audioUrl = URL.createObjectURL(audioBlob);
    });

    setTimeout(() => {
      mediaRecorder.stop();
    }, 3000);
  });

  navigator.mediaDevices.getUserMedia({ audio: true })
  .then(stream => {
    const mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.start();

    const audioChunks = [];
    mediaRecorder.addEventListener("dataavailable", event => {
      audioChunks.push(event.data);
    });

    mediaRecorder.addEventListener("stop", () => {
      const audioBlob = new Blob(audioChunks);
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      audio.play();
    });

    setTimeout(() => {
      mediaRecorder.stop();
    }, 3000);
  });

  const recordAudio = () => {
  return new Promise(resolve => {
    navigator.mediaDevices.getUserMedia({ audio: true })
      .then(stream => {
        const mediaRecorder = new MediaRecorder(stream);
        const audioChunks = [];

        mediaRecorder.addEventListener("dataavailable", event => {
          audioChunks.push(event.data);
        });

        const start = () => {
          mediaRecorder.start();
        };

        const stop = () => {
          return new Promise(resolve => {
            mediaRecorder.addEventListener("stop", () => {
              const audioBlob = new Blob(audioChunks);
              const audioUrl = URL.createObjectURL(audioBlob);
              const audio = new Audio(audioUrl);
              const play = () => {
                audio.play();
              };

              resolve({ audioBlob, audioUrl, play });
            });

            mediaRecorder.stop();
          });
        };

        resolve({ start, stop });
      });
  });
};

(async () => {
  const recorder = await recordAudio();
  recorder.start();

  setTimeout(async () => {
    const audio = await recorder.stop();
    audio.play();
  }, 3000);
})();

const sleep = time => new Promise(resolve => setTimeout(resolve, time));

(async () => {
  const recorder = await recordAudio();
  recorder.start();
  await sleep(3000);
  const audio = await recorder.stop();
  audio.play();
})();

const recordAudio = () =>
  new Promise(async resolve => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream);
    const audioChunks = [];

    mediaRecorder.addEventListener("dataavailable", event => {
      audioChunks.push(event.data);
    });

    const start = () => mediaRecorder.start();

    const stop = () =>
      new Promise(resolve => {
        mediaRecorder.addEventListener("stop", () => {
          const audioBlob = new Blob(audioChunks);
          const audioUrl = URL.createObjectURL(audioBlob);
          const audio = new Audio(audioUrl);
          const play = () => audio.play();
          resolve({ audioBlob, audioUrl, play });
        });

        mediaRecorder.stop();
      });

    resolve({ start, stop });
  });

const sleep = time => new Promise(resolve => setTimeout(resolve, time));

(async () => {
  const recorder = await recordAudio();
  recorder.start();
  await sleep(3000);
  const audio = await recorder.stop();
  audio.play();
})();