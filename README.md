### 😮 What this bot can do
BOT can easily join to public and private groups, Scan members and fetch Phone Numbers, Usernames and UserIDs

Then Scan all group messages to find any phone numbers in the texts.

__This is a small part of big project with a CLI bot that made by python and pyrogram and maybe update later!__

#### ⚠️⚠️ **The consequences of misuse are your own** ⚠️⚠️

### 🚀 Automatic Download
Clone this repository with this command

```bash
git clone https://github.com/RealMrHex/tele-finder.git
``` 

### ✋ Manual Download
You can freely download __Core.py__ file and edit it!.


### ⚙️ Setup
Run this commands to install __Pyrogram__ and __Tgcrypto__
```bash
pip3 install -U pyrogram

pip3 install -U tgcrypto
``` 

🔷 Set your telegram account __API_ID__ and __API_HASH__
```bash
LINE 9  : api_id   = 'YOUR API ID'
LINE 10 : api_hash = 'YOUR API HASH'
```

### 😎 Almost Done...!

Run the script and enjoy!

### 😨 Oppps!!! We forgot the usage

#### 🔗 For public groups, send message with the following format in any chat you want!
```php
[join] ID

✍️ e.g: [join] laravelGroup
```

#### 🔓 For private groups, send message with the following format in any chat you want!
```php
[join] INVITE_LINK

✍️ e.g: [join] https://t.me/+103255xxxacxxxxx
```

### 🤓 Explanation
```yaml
Status           : Current status
Target           : Target chat title
Members          : Target members count
Scanned          : Total scanned accounts
Founded Phones   : Founded phone numbers
Founded Usernames: Founded usernames like @Logcats
Founded User IDs : Founded user IDs like 123456789
Hex              : Special format of all data ---> Phone:Username:User-id 
Founded M-Phones : Founded phone numbers in group messages
Scanned Messages : Scanned message for finding phone numbers.
```

### 😤 Bad Usage
#### DO NOT Scan multiple chats AT ONCE.
#### When the process end, bot send a message that notify you about the process status, please wait until you get the message!
#### DO NOT Scan a chat for multiple times on a short period.



### 🔎 Security

If you discover any security related issues, please email `hex@kaqaz.studio` instead of using the issue tracker.

### Credits

- [Armin Hooshmand](https://github.com/realmrhex) ([CV](https://hex.kaqaz.studio))
- [Kaqaz Studio Corp](https://github.com/kaqazstudio) ([Website](https://kaqaz.studio))
- [All Contributors](../../contributors)

### License

The MIT License (MIT). Please see [License File](LICENSE.md) for more information.
