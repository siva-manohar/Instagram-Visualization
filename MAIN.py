import scrape
import convert

""" SETTINGS """
username = 'peoplebesnoopin'
password = 'Arduinopro'

scanName = 'cam.tan'
scanNumber = 29

scrape.runScan(username, password, scanName, scanNumber)
convert.processFile(scanName)