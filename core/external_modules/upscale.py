def upscale(speak,logger):
    try:
        import cv2
        from cv2 import dnn_superres
        from os import listdir
        from os.path import isfile, join
        speak("Loading upscale ai models")
        onlyfiles = [f for f in listdir("../modules_files/folders/upscale_models/") if isfile(join("upscale_models/", f))]
        print(onlyfiles)
        # Create an SR object
        sr = dnn_superres.DnnSuperResImpl_create()
        speak("Provide the image")
        im = input("image name: ")
        # Read image
        image = cv2.imread(im)

        # Read the desired model
        path = "upscale_models/FSRCNN_x2.pb"
        sr.readModel(path)
        sr.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        sr.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        # Set the desired model and scale to get correct pre- and post-processing
        sr.setModel("fsrcnn", 2)

        # Upscale the image
        result = sr.upsample(image)

        # Save the image
        cv2.imwrite(im+"x.png", result)
        speak("The image has been upscaled successfully")
    except Exception as e:
            print(str(e))
    