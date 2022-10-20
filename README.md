
![Logo](M.I.A.-logo.png)


# M.I.A

AI Assistant for day to day life


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file


`EMAILER_MAIL_FOR_SEND`
`ADMIN_MAIL`
`CARTER_KEY`
`OPENWEATHER_API`
`WOLFRAMALPTH_KEY1`
`WOLFRAMALPTH_KEY2`
`ADMIN_PASS_LIST_SHA512`
`USER1`
`USER2`
`USERPASS1_SHA512`
`USERPASS2_SHA512`
`DEVICE_MODEL_ID`
`DEVICE_ID`
`GITHUB_TOKEN`

This is necessary only to make your own update and distribute it

`UPDATE_DATABASE_HOST`
`UPDATE_DATABASE_USERNAME`
`UPDATE_DATABASE_PASS`


## Run Locally

Clone the project

1. Put the Goolge Assistant API token file in ```M.I.A/data/token.json```

2. Put ffmpeg.exe, ffplay.exe, ffprobe.exe in ```M.I.A./``` folder from https://ffmpeg.org/download.html

3. Start the assistant

```bash
  python3 .\start_M.I.A.py
```

If there is an problem with the auto libraries install then run

```bash
  pip install -r requirement.txt
```
