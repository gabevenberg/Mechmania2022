import zipapp
print("Writing to bot.pyz...")
zipapp.create_archive('./src', main='main:main', target='bot.pyz')
print("Done!")
