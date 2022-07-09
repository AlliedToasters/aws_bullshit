# AWS Bullshit
Here documents how to deal with AWS bullshit (wrt your local env.)

## Activate a profile
seems like a lot of `aws` commands ignore the active profile and just use these env variables:

```
$AWS_ACCESS_KEY_ID
$AWS_SECRET_ACCESS_KEY
```

so `activate_profile.py` simply resets these env variables.

## Usage

Run the script:

```
python activate_profile.py --profile <PROFILE>
```
if it works, you'll be prompted to reactivate your .zshrc:
```
source ~/.zshrc
```
that's it.
