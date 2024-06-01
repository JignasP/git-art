from datetime import datetime, timedelta
import calendar
from PIL import Image
import git
import os



def convert_img(img_path,new_width,new_height = 7):

    img = Image.open(img_path)
    commit_no = [0, 2, 4, 8, 13]


    img = img.resize((new_width,new_height)).convert('L')
    pix = []

    for x in range(img.size[0]):
        for y in range(img.size[1]):

            color = img.getpixel((x, y))

            pix.append(commit_no[int(color / 255 * (len(commit_no)-1))])

    return pix


def create_commit_on_date(local_path,repo, commit_date, commit_message="Backdated commit"):
    # Create a git commit on a specific date.


    with open(f'{local_path}/file.txt', 'a') as file:
        file.write(f'\n{commit_date}')

    repo.git.add(A=True)

    repo.index.commit(commit_message, author_date=commit_date,commit_date=commit_date)


def get_first_monday_and_last_friday(year):

    # Get the first Monday and last Friday of the given year.
    first_day_of_year = datetime(year, 1, 1)
    last_day_of_year = datetime(year, 12, 31)

    # Calculate first Monday
    first_monday = first_day_of_year + timedelta(days=(calendar.MONDAY - first_day_of_year.weekday() + 6) % 7)

    # Calculate last Friday
    last_friday = last_day_of_year - timedelta(days=(last_day_of_year.weekday() - calendar.FRIDAY + 6) % 7)

    weeks = ((last_friday - first_monday).days // 7)+1



    return first_monday, last_friday, weeks

def main():
    repo_url = input("Enter the repo url: ")
    local_path = input("Enter the local path: ")
    token = input("Enter the Personal Access Token : ")

    # Create the remote URL with the token
    repo_url_with_token = repo_url.replace('https://', f'https://{token}@')

    # Clone the repository if not already cloned
    if not os.path.exists(local_path):
        repo = git.Repo.clone_from(repo_url_with_token, local_path)
    else:
        repo = git.Repo(local_path)


    img_path = input("Enter the path to your image: ").strip()
    year = int(input("Enter the year: "))



    start_date, end_date, weeks = get_first_monday_and_last_friday(year)
    current_date = start_date
    print(weeks)
    pix=convert_img(img_path,weeks)
    day_no= 0

    print(start_date, end_date, weeks)
    print("date",end_date)

    while current_date <= end_date:
        commit_date = current_date.strftime("%Y-%m-%dT%H:%M:%S")

        print(current_date)

        for i in range(0,pix[day_no]):
            create_commit_on_date(local_path,repo, commit_date)

        origin = repo.remote(name='origin')
        origin.push()

        current_date += timedelta(days=1)
        day_no +=1

    origin = repo.remote(name='origin')
    origin.push()
    print("Finished creating backdated commits.")

if __name__ == "__main__":
    main()
