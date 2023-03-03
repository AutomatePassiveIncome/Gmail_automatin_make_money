Code 1
#@title **install verify_email**
!pip install verify_email 

Code 2
#@title **Search Emais and save**

import csv, re, requests, time, sys, random, smtplib, ssl, random
from bs4 import BeautifulSoup
from verify_email import verify_email
from email.message import EmailMessage

email_provides_file = '/content/drive/MyDrive/Emails/ep.csv'
row_emails_file = '/content/drive/MyDrive/Emails/row_emails.csv'
no_duplicates_file = '/content/drive/MyDrive/Emails/row_removed_duplicates.csv'
emails_file = '/content/drive/MyDrive/Emails/emails.csv'
all_user_file = '/content/drive/MyDrive/Emails/all_user.csv'
user_file = '/content/drive/MyDrive/Emails/user.csv'
emalis_file = '/content/drive/MyDrive/Emails/emails.csv'
emials_teplate_folder = '/content/drive/MyDrive/Emails/emails_template/message'

counter_all_users = 0
counter_save_email_loop = 0


def remove_duplicates_from_row_file():
  seen_lines = set()
  with open(row_emails_file, 'r') as csv_input:
    with open(no_duplicates_file, 'w', newline='') as csv_output:
        reader = csv.reader(csv_input)
        writer = csv.writer(csv_output)
        for row in reader:
            line = row[0]  
            if line not in seen_lines:
                writer.writerow([line])
                seen_lines.add(line)
        with open(row_emails_file, 'w') as csv_input:
          pass

def remove_first_line(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        lines.pop(0)
    with open(filename, 'w') as file:
        file.writelines(lines)

def verify_emails_and_save():
  rows = []
  with open(no_duplicates_file, 'r') as i_f:
    for line in i_f:
      email = line.strip()
      verify_emails = verify_email(email)
      if verify_email:
        rows.append([email])
        with open(emails_file, "w", newline='') as o_f:
          writer = csv.writer(o_f)
          writer.writerows(rows)
          remove_first_line(no_duplicates_file)
      else:
        remove_first_line(no_duplicates_file)
def save_all_users_to_file():
  global counter_all_users
  if counter_all_users == 0:  
    with open(all_user_file, 'r') as input_file, open(user_file, 'w', newline='') as output_file:
      reader = csv.reader(input_file)
      writer = csv.writer(output_file)
      header = next(reader)
      writer.writerow(header[:2])
      for row in reader:
          writer.writerow(row[:2])
      counter_all_users += 1 
      print("All users save", counter_all_users)

def send_emails_loop():
  replyto = 'airobot2023@gmail.com'
  subject = '$500 Free Google Ads credit With Social Media Advertising with A.I.'
  name = 'Adcreative.ai Team.'

  counter = {}
  counter_all = 0

  with open(user_file) as f:
      data = [row for row in csv.reader(f)]

      file_list = [emials_teplate_folder + str(i) + '.txt' for i in range(1,11)]
      

  with open(emalis_file, 'r') as csvfile:
      datareader = csv.reader(csvfile)
      for row in datareader:
          random_user = random.choice(data)
          sender = random_user[0]
          password = random_user[1]
          if sender not in counter:
              counter[sender] = 0
          
          if counter[sender] >= 500:
              continue
          try:
              context = ssl.create_default_context()
              server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)
              server.login(sender, password)
              em =EmailMessage()
              em['from'] = f'{name} <{sender}>'
              em['Reply-To'] = replyto
              em['To'] = row
              em['subject'] = subject
              random_file = random.choice(file_list)
              with open(random_file, 'r') as file:
                  html_msg = file.read()
              em.add_alternative(html_msg, subtype='html')
              server.send_message(em)
              counter[sender] += 1
              counter_all += 1
              print(counter[sender], " emails sent", "From ", sender,  "To ", row ,"File ", random_file)
              with open(emalis_file, "r") as file:
                  reader = csv.reader(file)
                  rows = list(reader)
                  rows = rows[1:]
              if rows:
                  with open(emalis_file, "w", newline='') as file:
                      writer = csv.writer(file)
                      writer.writerows(rows)
              server.close()
          except Exception as e:
              print(f"Error sending email From {sender} to {row}:", e) 
              if "550, b'5.4.5 Daily user sending quota exceeded" in str(e):
                  print(f"Removing {sender} from user.csv")
                  with open(user_file, "r") as file:
                      reader = csv.reader(file)
                      rows = list(reader)
                  with open(user_file, "w", newline='') as file:
                      writer = csv.writer(file)
                      for r in rows:
                          if r[0] != sender:
                              writer.writerow(r)
                      data = [row for row in rows]
              elif "Please log in with your web browser and then try again." in str(e):
                  print(f"Removing {sender} from user.csv")
                  with open(user_file, "r") as file:
                      reader = csv.reader(file)
                      rows = list(reader)
                  with open(user_file, "w", newline='') as file:
                      writer = csv.writer(file)
                      for r in rows:
                          if r[0] != sender:
                              writer.writerow(r)
                      data = [row for row in rows]
              elif "https://accounts.google.com/signin/continue" in str(e):
                  print(f"Removing {sender} from user.csv")
                  with open(user_file, "r") as file:
                      reader = csv.reader(file)
                      rows = list(reader)
                  with open(user_file, "w", newline='') as file:
                      writer = csv.writer(file)
                      for r in rows:
                          if r[0] != sender:
                              writer.writerow(r)
                      data = [row for row in rows]

              with open(emalis_file, "r") as file:
                  reader = csv.reader(file)
                  rows = list(reader)
                  rows = rows[1:]
              if rows:
                  with open(emalis_file, "w", newline='') as file:
                      writer = csv.writer(file)
                      writer.writerows(rows)
  for sender, count in counter.items():
      print(f"{sender}: {count}")
  print("Emails Sent", counter_all)


def save_emails():
  while True:
    email_providers = []
    with open(email_provides_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            email_providers.append(row[0])
    site = "myshopify.com"
    random_number = random.randint(1, 999)
    emails = []
    for provider in email_providers:
      url = f'https://www.google.com/search?q={random_number}+"{provider}"+"{site}"+location:usa'
      response = requests.get(url)
      print(url)
      content = response.content
      soup = BeautifulSoup(content, 'html.parser')
      text = ' '.join([t.strip() for t in soup.stripped_strings])
      if "please enable javascript on your web browser." in text:
        print("Done Try again ")
        sys.exit()
      else:
        time.sleep(2)
      
      email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
      emails += re.findall(email_regex, text)
      with open(row_emails_file, 'a', newline='') as f:
          writer = csv.writer(f)
          for email in emails:
              writer.writerow([email])
      print("emails Saved to row.csv file")
      time.sleep(2)
    remove_duplicates_from_row_file()
    print("Removed Duplicates and saved to no_duplicate.csv file")
    time.sleep(1)
    verify_emails_and_save()
    print("verify emails and save to emalis.csv file")
    if counter_all_users == 0:
      save_all_users_to_file()
    send_emails_loop()
    print('Emails sent and wationg 20 se')
    time.sleep(5)
save_emails()