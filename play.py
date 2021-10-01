from PIL import Image, ImageDraw, ImageFont
# get an image
base_size = (400,200)

cnv = Image.new("RGBA", base_size, (255,255,255,255))

# get a font
d = ImageDraw.Draw(cnv)
min_dim = (min(base_size),min(base_size))
pos = ((base_size[0]-min_dim[0])//2,(base_size[1]-min_dim[1])//2)
size = pos[0]+min_dim[0],pos[1]+min_dim[1]
#d.ellipse(pos+size, fill=(0,0,0,255))
print(pos+size)
#cnv.show()

pos = ((base_size[0]-min_dim[0])//2,(base_size[1]-min_dim[1])//2)
size = pos[0]+min_dim[0],pos[1]+min_dim[1]
pt_1 = (pos[0],size[1])
pt_2 = (pos[0]+(min_dim[0]//2),pos[1])
pt_3 = size
d.polygon([pt_1,pt_2,pt_3],fill=(0,1,0,255))

cnv.show()

