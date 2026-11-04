import qrcode

text = "Ivan Petrenko, PZ-11, ivan.petrenko@example.com"
image = qrcode.make(text)
image.save("contact.png")
print("saved: contact.png")
