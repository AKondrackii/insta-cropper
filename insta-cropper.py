import os, sys
from PIL import Image, ImageOps

def get_files(subfolders: bool = False) -> list:
  root = os.getcwd()

  not_filtered_files = []
  
  if subfolders == True:
    # pylint: disable=unused-variable
    for path, subdirs, files in os.walk(root):
      for name in files:
        not_filtered_files.append(os.path.join(path, name))
  else:
    not_filtered_files = list(
      map(
        lambda y: root + os.sep + y,
        filter(
          lambda x:
            (len(x.split('.')) >= 2) and
            (str(x.split('.')[0]) != ''),
          os.listdir(root)
        )
      )
    )

  return not_filtered_files

def filter_files(allow_formats: list, files: list) -> list:
  print(allow_formats)
  filtered_files = list(
    filter(
      lambda f:
        (f.split(os.sep)[-1])
          .split('.')[-1]
        in allow_formats,
      files
    )
  )

  return filtered_files

def image_proccessing(path_to_image: str) -> None:
  try:
    image = Image.open(path_to_image)
  except IOError:
    print("Cant open image!")
    sys.exit(1)

  original_name = path_to_image.split(os.sep)[-1].split('.')[-2]
  original_extension = path_to_image.split(os.sep)[-1].split('.')[-1]

  print('Opened: {}'.format(original_name + '.' + original_extension))

  original_width, original_height = image.size
  new_width = 0
  new_height = 0

  print('Original size: {0}x{1}'.format(original_width, original_height))

  if (
    round(
      original_width / original_height,
      1
    ) not in [
      0.8,
      1.2
    ]
  ) == True:
    if (original_height >= original_width):
      new_width = int(original_width * (4/5))
      new_height = original_height
    else:
      new_width = original_width
      new_height = int(original_height * (5/4))

    print('New size: {0}x{1}'.format(new_width, new_height))

    image = ImageOps.pad(
      image=image,
      size=(new_width, new_height),
      method=Image.BICUBIC,
      color=0x00FFFFFF,
      centering=(0, 0.5)
    )

    splitted_path_to_image = path_to_image.split(os.sep)
    splitted_path_to_image[-1] = original_name + '_4x5.' + original_extension

    new_path_to_image = os.sep.join(splitted_path_to_image)

    try:
      image.save(new_path_to_image)
    except IOError:
      print("Can't save image")
      sys.exit(1)

    print('Saved as: ', new_path_to_image)
  else:
    print('The image does not need to be resized! Skip...')

  print('\n')

def main(**kwargs) -> None:
  files = filter_files(
    allow_formats=['jpg', 'jpeg', 'png'],
    files=get_files(
      subfolders=kwargs.get('subfolders')
    )
  )

  for file in files:
    image_proccessing(file)

if __name__ == "__main__":
  subfolders = str(input('Check subfolders? (Y/n) ')).lower()

  if (subfolders == 'y' or
    subfolders == 'yes' or
    subfolders == 'д' or
    subfolders == 'да'):
    subfolders = True
  else:
    subfolders = False

  main(
    subfolders=subfolders
  )
