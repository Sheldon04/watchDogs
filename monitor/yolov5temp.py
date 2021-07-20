            # # Images
            # img = frame_lwpCV  # or file, PIL, OpenCV, numpy, multiple
            # # Inference
            # results = model(img)
            # # Results
            # # results.show()  # or .show(), .save(), .crop(), .pandas(), etc.
            # # print(type(results.pandas().xyxy[0]['xmin'].values[0]))
            # if len(results.pandas().xyxy[0]['xmin'].values) != 0:
            #     cv2.rectangle(frame_lwpCV, (
            #         int(results.pandas().xyxy[0]['xmin'].values[0]), int(results.pandas().xyxy[0]['ymin'].values[0])),
            #         (int(results.pandas().xyxy[0]['xmax'].values[0]), int(results.pandas().xyxy[0]['ymax'].values[0])),
            #             (255, 255, 0), 2)