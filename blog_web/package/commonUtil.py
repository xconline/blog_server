pageSize = 5
static_path = r'E:\projects\PycharmProjects\blog_web\blog_web\static\images'
server = r'localhost:8000'
imageBedUrl = 'https://raw.githubusercontent.com/xconline/images/master/'


def getLocalFromDateTime(dateTime):
    from tzlocal import get_localzone
    try:
        return dateTime.astimezone(get_localzone()).strftime('%y-%m-%d')
    except Exception as e:
        return dateTime


def get_fileType(type):
    if 'png' in type or 'PNG' in type:
        return 'png'
    elif 'jpg' in type or 'JPG' in type:
        return 'jpg'
