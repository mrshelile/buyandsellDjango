# buyandsellDjango

pip install -r requirements.txt

\# BuyAndSellDjango Deployment Overview



\## Repository Information

\- \*\*Repository Path:\*\* `/home/marakac1/repositories/buyandsellDjango`

\- \*\*Remote URL:\*\* \[https://github.com/mrshelile/buyandsellDjango.git](https://github.com/mrshelile/buyandsellDjango.git)

\- \*\*Current Branch:\*\* `production`

\- \*\*HEAD Commit:\*\* `Prepare for deployment` (latest changes ready for deployment)



\## Deployment Requirements

1\. \*\*.cpanel.yml file\*\*

&nbsp;  - Located in the repository root.

&nbsp;  - Defines deployment tasks including virtual environment setup, package installation, database migrations, and static file collection.



2\. \*\*Clean Git Status\*\*

&nbsp;  - No uncommitted changes.

&nbsp;  - All deployable changes are committed to the `production` branch.



\## Deployment Steps (cPanel)

1\. Navigate to \*\*Git™ Version Control → Pull or Deploy → Deploy\*\*.

2\. cPanel reads `.cpanel.yml` and executes tasks:

&nbsp;  - Create virtual environment

&nbsp;  - Install Python dependencies

&nbsp;  - Apply database migrations

&nbsp;  - Collect static files



\## Security Notes

\- GitGuardian has flagged hardcoded secrets in `buyandsellDjango/settings.py`.

\- Best practice: Move sensitive credentials to environment variables.

\- Rotate exposed credentials (SMTP, database passwords) as needed.



\## Branch Management

\- `production` branch is ahead of `master` by 41 commits.

\- For merging deployable changes to `master`:

&nbsp; ```bash

&nbsp; git checkout master

&nbsp; git merge production

&nbsp; git push origin master



