Since the SDK is currently not running properly on the EscpaePod and scripts are only occasionally executed without errors, I solved the problem with a cronjob.

Vector checks if it sees a face. If so, he tells a random joke, a fun fact, news, the time, the weather or greets you. It also checks the whether or if you have received a new email. When he sits on his charging station and is fully charged while he sees a face, he starts to play.

The 1-minute cron job between 6 a.m. and 9 p.m. works well for me. e.g.

* 6-21 * * * /home/ubuntu/cronVec/cronVec.py