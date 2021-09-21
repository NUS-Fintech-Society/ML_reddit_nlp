# Reddit Scraper
## Prerequisiets

Please ensure that you have **ZSTD, Bzip2, and XZ** utilites installed in your command-line.

Also ensure that your computer is equipped with basic packages, such as **Wget, tee (linux), and java (JDK 11 or above)**.

## Steps

1. Go to the below sites where Pushshift io maintains the monthly dumps.
   - https://files.pushshift.io/reddit/submissions/
   - https://files.pushshift.io/reddit/comments/
2. In the `Links` file, add download links of the files you wish to parse.
(e.g)
```
https://files.pushshift.io/reddit/submissions/RS_2006-01.zst
https://files.pushshift.io/reddit/submissions/RS_2006-02.zst
...
```
3. After saving the `Links` file, run the `start.sh` script.
(e.g)
```
./start.sh
```
4. All the scraped .csv files will be stored in `/data` folder.
