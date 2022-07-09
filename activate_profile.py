import os
import argparse

home = os.path.expanduser('~')

with open(os.path.join(home, '.aws', 'credentials'), 'r') as f:
    creds = f.read()
lines = creds.split('\n')
profile, key, key_id = None, None, None
output = {}
for line in lines:
    if '[' in line:
        if profile is not None:
            output[profile] = {
                'aws_access_key_id':key_id,
                'aws_secret_access_key':key
            }
        profile = line.split('[')[1].split(']')[0]
    if '=' in line:
        if line.split('=')[0].strip() == 'aws_access_key_id':
            key_id = line.split('=')[1].strip()
        elif line.split('=')[0].strip() == 'aws_secret_access_key':
            key = line.split('=')[1].strip()

output[profile] = {
    'aws_access_key_id':key_id,
    'aws_secret_access_key':key
}
    

parser = argparse.ArgumentParser()
parser.add_argument("profile", help="the name of the profile you want to activate.")
args = parser.parse_args()
input_profile = args.profile
if input_profile in output.keys():
    print('activating profile: ', input_profile)
    obj = output[input_profile]
    os.environ["AWS_ACCESS_KEY_ID"] = obj['aws_access_key_id']
    os.environ["AWS_SECRET_ACCESS_KEY"] = obj['aws_secret_access_key']
    os.environ["AWS_PROFILE"] = input_profile
    print('done!')
else:
    raise KeyError(f"profile {input_profile} not found in aws credentials.")


with open(os.path.join(home, '.zshrc'), 'r') as f:
    zshrc = f.read()

prof, ky, kyid = False, False, False
lines = zshrc.split('\n')
for i, line in enumerate(lines):
    if 'AWS_SECRET_ACCESS_KEY' in line:
        key_id = os.environ.get("AWS_ACCESS_KEY_ID")
        lines[i] = f"export AWS_ACCESS_KEY_ID={key_id}"
        kyid = True
    if 'AWS_ACCESS_KEY_ID' in line:
        key = os.environ.get("AWS_SECRET_ACCESS_KEY")
        lines[i] = f"export AWS_SECRET_ACCESS_KEY={key}"
        ky = True
    if 'AWS_PROFILE' in line:
        lines[i] = f"export AWS_PROFILE={input_profile}"
        prof = True

if not kyid:
    lines.append(f"export AWS_ACCESS_KEY_ID={key_id}")
if not ky:
    lines.append(f"export AWS_SECRET_ACCESS_KEY={key}")
if not prof:
    lines.append(f"export AWS_PROFILE={input_profile}")
output = '\n'.join(lines)
with open(os.path.join(home, '.zshrc'), 'w') as f:
    f.write(output)

print('updated .zshrc. please reactatve with:')
print('source ~/.zshrc')
