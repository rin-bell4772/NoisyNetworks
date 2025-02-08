# NoisyNetworks

Creator: Rin Takahashi

## Purpose
A cute web app where cats ping websites and sing!
Something Fun!

## Tools utilized
- Streamlit

## Challenges

Challenge 1:
Messing with audio in python is fun but there are a lot of different libraries and some of them work for different use cases. In my case, I started using the simpleaudio library, but unfortunately it is incompatible with headless machines (servers). As streamlit's cloud community is based off of linux servers, this had to be completely replaced with another python audio library. simpleaudio was replaced with pydub. pydub was simpler to use and was compatible with servers. 
However, Something I didn't consider was how the browser would play the audio. Yes, pydub is compatible with headless applications, but it is still not able to forward that audio output to the client browser. 
So, I had to use Streamlit's audio api, which was not difficult.

Challenge 2:
Deploying to Streamlit Cloud Community was certainly not as easy as writing it. I ran into many issues with dependencies and libraries, however I believe a majority of these issued were my own fault.
This was when I realized I had to change my python audio library as well.

## Credits:
- Ascii art from ASCII Art Archive (https://www.asciiart.eu/)
