An aiohttp stream server for DeepSpeech
=======================================

Implements a full asynchronous HTTP server for converting speech to text in
realtime using [DeepSpeech][].

Since version [0.2][DeepSpeech Streaming], DeepSpeech has supported streaming
APIs that allow processing audio data in small chunks instead of all at once.
This enables the capability of a real-time streaming server (given sufficient
hardware). 

Real time streaming of audio data requires that both client and server support
[HTTP chunks][] so that data can be passed from the client to the server in
small batches. This allows the server to start processing the data with
DeepSpeech while more data is being recorded and transferred by the client.

Usage
-----

This project uses [Pipenv][] to manage dependencies. To install the dependencies
and get a shell, run: `pipenv install && pipenv shell`

Once in that, shell, simply run `./app.py` to start the server.


Results
-------

The preliminary results from this implementation are very encouraging. On my
dual-core i5-6200 laptop, the server is easily able to keep up with a realtime
stream of audio data from the microphone:

**Client:**
```
$ ./examples/mic http://localhost:8080/stt
rec WARN wav: Length in output .wav header will be wrong since can't seek to fix it

Input File     : 'default' (pulseaudio)
Channels       : 1
Sample Rate    : 16000
Precision      : 16-bit
Sample Encoding: 16-bit Signed Integer PCM

In:0.00% 00:00:05.63 [00:00:00.00] Out:55.8k [      |      ]        Clip:0
Done.
the quick brown fox jumped over the lazy dog
```

**Server**
```
$ ./app.py
INFO:root:Loading model...
TensorFlow: v1.12.0-10-ge232881
DeepSpeech: v0.4.1-0-g0e40db6
2019-06-05 09:54:49.098465: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
INFO:root:Model was loaded in 0.236s
======== Running on http://0.0.0.0:8080 ========
(Press CTRL+C to quit)
INFO:root:Processing Stream...
INFO:root:Inference took 1.751s for 3.486s audio sample with 0.249s latency. Total time: 7.098s
```

As can be seen, the server was easily able to process the streamed audio data
about twice as fast as it was streamed. In addition, the minimal latency (time
from when the last audio sample was received to the time when the server sent a
response to the client) meant that the server was able to respond back to the
client very promptly once the audio clip was finished.


[DeepSpeech]: https://github.com/mozilla/DeepSpeech
[DeepSpeech Streaming]: https://hacks.mozilla.org/2018/09/speech-recognition-deepspeech/
[HTTP chunks]: https://en.wikipedia.org/wiki/Chunked_transfer_encoding
