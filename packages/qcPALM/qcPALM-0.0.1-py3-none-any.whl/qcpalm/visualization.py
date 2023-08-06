import numpy as np

def visualize(x_arr, y_arr, cross_size = 2, threshold = False, border_width = 10, 
              longest_axis_length = 800, dpi = 80, show_visualization = True):
    '''
    Visualizes super-resolution localizations at positions (`x_arr`, `y_arr`)
    as crosses with radius `cross_size` and returns array representing visualization
    
    Parameters
    ----------
    x_arr : array_like
        One-dimensional array containing the x-coordinates of localizations.
    y_arr : array_like
        One-dimensional array containing the y-coordinates of localizations.
    cross_size : int, default 2
        Radius of cross for visualization.
    threshold : bool, default False
        Whether all pixels containing any signal should be set to 1.
    border_width : int, default 10
        Number of pixels bordering localizations. Must be greater than `cross_size`.
    longest_axis_length : int, default 800
        Number of pixels that the longest axis of the image should span.
    dpi : int, default 80
        Dots per inch of the visualization
    show_visualization : bool, default True
        Whether to display the resulting array or not
    
    Returns
    -------
    roi_arr : 2darray
        Two-dimensional array populated with the localizations modified according 
        to the visualization parameters above
    '''
    # Check which axis of image is longer
    longer_axis = 'x'
    if np.max(y_arr) > np.max(x_arr):
        longer_axis = 'y'
        
    # Scale `x_arr` and `y_arr` to minimum values --> 0
    x_arr = x_arr - np.min(x_arr)
    y_arr = y_arr - np.min(y_arr)
     
    # Scale longer axis of image to visualization parameters
    if longer_axis == 'x':
        # Scaling `x_arr` and `y_arr` from um to px
        scaling_parameter = (longest_axis_length - 2*border_width)/\
                             (np.max(x_arr)-np.min(x_arr)) # Compute scaling parameter, px/um
        x_arr_px = border_width + x_arr*scaling_parameter
        y_arr_px = border_width + y_arr*scaling_parameter
        
        # Compute scaled ROI dimensions
        x_roi = longest_axis_length
        y_roi = int(np.round(longest_axis_length * (np.max(y_arr)+(2*border_width/scaling_parameter))/\
                             (np.max(x_arr)+(2*border_width/scaling_parameter))))
    else:
        # Scaling `x_arr` and `y_arr` from um to px
        scaling_parameter = (longest_axis_length - 2*border_width)/(np.max(y_arr)-np.min(y_arr)) 
        # Compute scaling parameter, px/um
        x_arr_px = border_width + x_arr*scaling_parameter
        y_arr_px = border_width + y_arr*scaling_parameter
        
        # Compute scaled ROI dimensions
        x_roi = int(np.round(longest_axis_length * (np.max(x_arr)+(2*border_width/scaling_parameter))/\
                             (np.max(y_arr)+(2*border_width/scaling_parameter))))
        y_roi = longest_axis_length
        
    # Initialize blank ROI array
    roi_arr = np.zeros((x_roi, y_roi))
    
    # (if) Visualize without crosses________________________________________
    if cross_size == 0:
        for i, j in zip(x_arr_px, y_arr_px):
            i_round, j_round = int(np.round(i)), int(np.round(j))
            roi_arr[i_round, j_round] = roi_arr[i_round, j_round] + 1    
        
    # (if) Visualize with crosses___________________________________________
    if cross_size > 0:
        for i, j in zip(x_arr_px, y_arr_px):
            i_round, j_round = int(np.round(i)), int(np.round(j))
            for k in range(-cross_size, cross_size + 1):
                roi_arr[i_round + k, j_round] = roi_arr[i_round + k, j_round] + 1
                roi_arr[i_round, j_round + k] = roi_arr[i_round, j_round + k] + 1

                roi_arr[i_round-1, j_round-1] = roi_arr[i_round-1, j_round-1] + .25
                roi_arr[i_round+1, j_round+1] = roi_arr[i_round+1, j_round+1] + .25
                roi_arr[i_round-1, j_round+1] = roi_arr[i_round-1, j_round+1] + .25
                roi_arr[i_round+1, j_round-1] = roi_arr[i_round+1, j_round-1] + .25

    # (if) Threshold: set all non-zero values to 1
    if threshold == True:
        roi_arr[roi_arr > 0] = 1
    
    # Visualize image_______________________________________________________
    if show_fig == True:
        plt.figure(figsize = (np.round(x_roi/dpi), np.round(y_roi/dpi)), dpi = dpi)
        plt.imshow(np.transpose(roi_arr), cmap='gist_heat', origin = 'lower')
        plt.show() 
        
    return roi_arr