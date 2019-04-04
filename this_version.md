Log of items changed since last commit:

- changed sunrise and sunset routine automation to trigger on - 4.0 solar angle;
  the solar angle and the number of minutes different from sunset/sunrise is
  written to a Google Sheet.
- replaced ClickSend with AWS Lambda script to send SMS text in "away stuff is on"
