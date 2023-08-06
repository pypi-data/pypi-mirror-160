# ⏲ ⏰ 🕰️ Fastimer

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

It is a little CLI timer to track fasts, designed specifically to help you monitor your fasting intervals, so you can optimize your results.  

 ## 😮 What's this for? There are a lot of apps like this!

Well, I wrote this one out of annoyance when [Zero](https://www.zerolongevity.com/) once again refused to show me the statistics it accumulates. Like, I tap on the calendar, but it does nothing. Geez-Louise!

It's not that hard, after all, so I just did it on my own.

## 🙃 How to install it?

```commandline
pip install fastimer
```

## 🙂 How to use it?

```commandline
fastimer
```

The script shows you a menu with three commands available: 

1. Display Fast
2. Start Fast
3. End Fast

The first one shows you how active fast is going on. For instance:

```
CURRENT FAST:    16 HOURS

Elapsed time:    00:38:27
Remaining:       15:21:33
        
Started:  Wed, 21:15
Goal:     Thu, 13:15
```

The second command starts a new fast, and the third one ends the active one.

## 😌 Where I can see or edit my fasts?

The script stores all the fasts in `journal.yaml` file in the working directory. The file is quite human-readable, so you can just open it in your lovely text editor.

For instance, the completed fast in the journal looks like this:

```yaml
- length: 16
  started: 2022-07-20 19:59:14.210099
  stopped: 2022-07-21 12:00:33.906634
```

The first parameter is the length of the fast, the second is the start date of this, and the third is the completion date.