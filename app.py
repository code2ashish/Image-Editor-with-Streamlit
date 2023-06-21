import streamlit as st

from PIL  import Image
import numpy as np
import cv2
import io
# Set the title of the app
st.title('Image Uploader')

# Create a file upload widget
image_file = st.file_uploader('Upload an image', type=['jpg', 'png'])

# print(type(image_file))



# If the user uploads an image
if image_file is not None:

    image = np.array(Image.open(image_file))

    k1,k2,k3 = st.columns(3)
    # Read the image file
    with k1:
        pass
    
    with k2:
        st.image(image,caption='Orignal',width=300)
    with k3:
        pass

    

    st.markdown('<span style="color:red; font-size:24px">Select Fillers</span>', unsafe_allow_html=True)

    options = st.multiselect(
        '🎞',
        ['grayscale', 'Brightness', 'Blur', 'Edge Detection'],
        [])
   
    cols,rows,_ = image.shape
    # print(rows, cols)
    processimage = image
    col1 , col2 = st.columns(2)
    opration_flag = False
    with col1:

        
        if options:
           
            for op in options:
                if op == 'grayscale':
                    
                    # processimage = cv2.cvtColor(processimage , cv2.COLOR_GRAY2RGB)
                    processimage = cv2.cvtColor(processimage ,cv2.COLOR_RGB2GRAY)
                    opration_flag = True
                if op == 'Brightness':
                    # st.write('Select Brightness factor')
                    brightness_factor = st.slider('Brightness', min_value=0, max_value= 100, value= 20)
                    
                    fl_image = processimage.astype('float')
                    adjusted_image = fl_image * brightness_factor/20

                    # Clip the pixel values to the valid range [0, 255]
                    adjusted_image = np.clip(adjusted_image, 0, 255)
                    
                    # Convert the image back to unsigned 8-bit integers
                    processimage = adjusted_image.astype(np.uint8)

                    # Clip the pixel values to the valid range [0, 255]
                    adjusted_image = np.clip(adjusted_image, 0, 255)
                    
                    # Convert the image back to unsigned 8-bit integers
                    processimage = adjusted_image.astype(np.uint8)
                    opration_flag = True
                if op == 'Blur':
                    # st.write('Select Blur value')
                    k = st.slider('Blur', min_value= 1, max_value= 20, value= 4)
                    
                    processimage = cv2.blur(processimage , ksize=(k,k))
                    opration_flag = True
                if op == 'Edge Detection':
                    # st.write('Edge Detection Slider')
                    th_lower = st.slider('Lower Thresold', min_value=1, max_value= 100, value= 50)
                    th_upper = st.slider('Upper Thresold', min_value=101, max_value= 200, value= 150 )

                    
                    processimage = cv2.Canny(processimage , threshold1=th_lower , threshold2= th_upper)
                    opration_flag = True

    with col2:
    

            if opration_flag:
                
                st.image(processimage,caption='Transformed',width=300)
                # img = Image.fromarray(processimage)

                # img.save(processimage , 'Download.png')
                cv2.imwrite('Download_filters.png' , cv2.cvtColor(processimage, cv2.COLOR_RGB2BGR))

                
                    
                with open('Download_filters.png' , 'rb') as opened_image:
                    btn = st.download_button(
                        label="Download image",
                        data=opened_image,
                        file_name="Download.jpg",
                        mime="image/png")
            
                # st.download_button(Image.fromarray(processimage),"Download.png", )
    

    st.markdown('<span style="color:red; font-size:24px">Select Transformation</span>', unsafe_allow_html=True)

    transformation = st.multiselect(
        '🤖',
        ['Resize', 'Rotation', 'Crop'],
        [])
    transform_flag = False

    transform_image = processimage

    c1 ,c2 = st.columns(2)

    with c1:


        if transformation:

            for t in transformation:
                if t== 'Rotation':
                    c ,r = transform_image.shape[1],transform_image.shape[0]

                    rot  = st.slider('Rotation Angle', min_value=-90, max_value= 90, value= 0)
                    M = cv2.getRotationMatrix2D((c//2,r//2),rot,1) 

                    
                    transform_image = cv2.warpAffine(transform_image,M,(c,r)) 

                    # transform_image = cv2.cvtColor(transform_image , cv2.COLOR_BGR2RGB)
                    cols ,rows =c , r

                    transform_flag = True

                        


            
                if t== 'Resize':
                    resize_facor  = st.slider('Resize', min_value=10, max_value= 200, value= 100)

                    transform_image = cv2.resize(transform_image , (cols*resize_facor//100 ,rows*resize_facor//100 ))
                    
                    transform_flag = True

                    


                if t== 'Crop':
                    X1  = st.slider('Start: x', min_value=0, max_value= rows, value= 0)
                    height = st.slider('Height', min_value=0, max_value= rows, value= rows)

                    X2 = st.slider('Start: y', min_value=0, max_value= cols, value= 0)
                    width = st.slider('Width', min_value=0, max_value= cols, value= cols)

                    transform_image = transform_image[X1:X1+height , X2:X2+width]
                    
                    

                    transform_flag = True

    with c2:
    

            if transform_flag:
                
                st.image(transform_image,caption='Transformed')
                # img = Image.fromarray(processimage)

                # img.save(processimage , 'Download.png')
                cv2.imwrite('Download_trans.png' , cv2.cvtColor(transform_image, cv2.COLOR_RGB2BGR))

                
                    
                with open('Download_trans.png' , 'rb') as opened_image:
                    btn = st.download_button(
                        label="Download final image",
                        data=opened_image,
                        file_name="Download.jpg",
                        mime="image/png")
            