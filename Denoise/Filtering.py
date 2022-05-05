
import numpy as np
class Filtering:

    def __init__(self, image, filter_name, filter_size, var = None):
        """initializes the variables of spatial filtering on an input image
        takes as input:
        image: the noisy input image
        filter_name: the name of the filter to use
        filter_size: integer value of the size of the fitler
        global_var: noise variance to be used in the Local noise reduction filter
        S_max: Maximum allowed size of the window that is used in adaptive median filter
        """

        self.image = image

        if filter_name == 'arithmetic_mean':
            self.filter = self.get_arithmetic_mean
        elif filter_name == 'geometric_mean':
            self.filter = self.get_geometric_mean
        if filter_name == 'local_noise':
            self.filter = self.get_local_noise
        elif filter_name == 'median':
            self.filter = self.get_median
        elif filter_name == 'adaptive_median':
            self.filter = self.get_adaptive_median

        self.filter_size = filter_size
        self.global_var = var
        self.S_max = 15

    def get_arithmetic_mean(self, roi):
        """Computes the arithmetic mean of the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the arithmetic mean value of the roi"""
        shape = roi.shape
        m = shape[0]
        n = shape[1]
        sum = 0
        for i in range(m):
          for j in range(n):
              sum = sum + roi[i,j]
        mean = sum/(m*n)

        
        return mean

    def get_geometric_mean(self, roi):
        """Computes the geometric mean for the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the geometric mean value of the roi"""
        shape = roi.shape
        m = shape[0]
        n = shape[1]
        sum = 1
        for i in range(m):
          for j in range(n):
              sum = sum*roi[i,j]
        gm = np.power(sum,1/(m*n))
        return gm

    def get_local_noise(self, roi):
        """Computes the local noise reduction value
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the local noise reduction value of the roi"""
        mean = self.get_arithmetic_mean(roi)
        size = self.filter_size
        global_var = self.global_var
        shape = roi.shape
        sum = 0
        count = 0
        for i in range(shape[0]):
            for j in range(shape[1]):
                sum = sum + (roi[i,j]-mean)**2
                count+=1
        variance = sum + mean*mean*(size*size-count)
        var = variance //(size*size)
        value = roi[shape[0]//2,shape[1]//2] - (global_var/var)*(roi[shape[0]//2,shape[1]//2]-mean)
        value = int(value)

        return value

    def get_median(self, roi):
        """Computes the median for the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the median value of the roi"""
        l = []
        shape = roi.shape
        for i in range(shape[0]):
          for j in range(shape[1]):
            l.append(roi[i,j])
        #sorting the list values
        ln = len(l)
        for i in range(ln):
            for j in range(i):
                if l[j] >= l[i]:
                    temp = l[j]
                    l[j] = l[i]
                    l[i] = temp
        #middle value is the median
        if ln%2 !=0:
            med = l[ln/2]
        else:
            a = ln/2
            b = ln/2 -1
            med = (l[a]+l[b])/2

        return med


    def get_adaptive_median(self,roi):
        """Use this function to implment the adaptive median.
        It is left up to the student to define the input to this function and call it as needed. Feel free to create
        additional functions as needed.
        """
        shape  = roi.shape
        sum = 0
        size = self.filter_size
        if shape[0] != size or shape[1] != size:
            return 0
        else:
            for i in range(shape[0]):
                for j in range(shape[1]):
                    sum = sum + (1/roi[i,j])
            value = size*size/sum
            return int(value)


    def filtering(self):
        """performs filtering on an image containing gaussian or salt & pepper noise
        returns the denoised image
        ----------------------------------------------------------
        Note: Here when we perform filtering we are not doing convolution.
        For every pixel in the image, we select a neighborhood of values defined by the kernal and apply a mathematical
        operation for all the elements with in the kernel. For example, mean, median and etc.

        Steps:
        1. add the necesssary zero padding to the noisy image, that way we have sufficient values to perform the operati
        ons on the pixels at the image corners. The number of rows and columns of zero padding is defined by the kernel size
        2. Iterate through the image and every pixel (i,j) gather the neighbors defined by the kernel into a list (or any data structure)
        3. Pass these values to one of the filters that will compute the necessary mathematical operations (mean, median, etc.)
        4. Save the results at (i,j) in the ouput image.
        5. return the output image

        Note: You can create extra functions as needed. For example if you feel that it is easier to create a new function for
        the adaptive median filter as it has two stages, you are welcome to do that.
        For the adaptive median filter assume that S_max (maximum allowed size of the window) is 15
        """
        image = self.image
        shape = image.shape
        size = self.filter_size

        l  = size -1
        l1 = l//2
        pd_image = np.zeros((shape[0]+l,shape[1]+l))
        pd_image[l1:l1+shape[0],l1:l1+shape[1]] = image
        out = np.zeros((shape[0],shape[1]))

        for i in range(l1,l1+shape[0]):
            for j in range(l2,l2+shape[0]):
               kernel = []
               for m in range(size):
                 for n in range(size):
                  p = m - l1
                  r = n - l1
                  kernel.append(pd_image[i+p,j+r])
               k = self.filter(kernel)
               out[i-l1,j-l1] = k

        return out

