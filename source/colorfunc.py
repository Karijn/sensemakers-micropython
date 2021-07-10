#import colorsys

def hsb2rgb(hsb):
    '''
    Transforms a hsb array to the corresponding rgb tuple
    In: hsb = array of three ints (h between 0 and 360, s and v between 0 and 100)
    Out: rgb = array of three ints (between 0 and 255)
    '''
    H = float(hsb[0] / 360.0)
    S = float(hsb[1] / 100.0)
    B = float(hsb[2] / 100.0)

    if (S == 0):
        R = int(round(B * 255))
        G = int(round(B * 255))
        B = int(round(B * 255))
    else:
        var_h = H * 6
        if (var_h == 6):
            var_h = 0  # H must be < 1
        var_i = int(var_h)
        var_1 = B * (1 - S)
        var_2 = B * (1 - S * (var_h - var_i))
        var_3 = B * (1 - S * (1 - (var_h - var_i)))

        if      (var_i == 0):
            var_r = B     ; var_g = var_3 ; var_b = var_1
        elif (var_i == 1):
            var_r = var_2 ; var_g = B     ; var_b = var_1
        elif (var_i == 2):
            var_r = var_1 ; var_g = B     ; var_b = var_3
        elif (var_i == 3):
            var_r = var_1 ; var_g = var_2 ; var_b = B
        elif (var_i == 4):
            var_r = var_3 ; var_g = var_1 ; var_b = B
        else:
            var_r = B     ; var_g = var_1 ; var_b = var_2

        R = int(round(var_r * 255))
        G = int(round(var_g * 255))
        B = int(round(var_b * 255))

    return [R, G, B]

def hsv_to_rgb(h, s, v):
    if s == 0.0: return [v, v, v]
    i = int(h*6.) # XXX assume int() truncates!
    f = (h*6.)-i; p,q,t = v*(1.-s), v*(1.-s*f), v*(1.-s*(1.-f)); i%=6
    if i == 0: return [v, t, p]
    if i == 1: return [q, v, p]
    if i == 2: return [p, v, t]
    if i == 3: return [p, q, v]
    if i == 4: return [t, p, v]
    if i == 5: return [v, p, q]

def HSV_2_RGB(HSV):
    ''' Converts an integer HSV tuple (value range from 0 to 255) to an RGB tuple '''

    # Unpack the HSV tuple for readability
    H, S, V = HSV

    # Check if the color is Grayscale
    if S == 0:
        R = V
        G = V
        B = V
        return (R, G, B)

    # Make hue 0-5
    region = H // 43

    # Find remainder part, make it from 0-255
    remainder = (H - (region * 43)) * 6

    # Calculate temp vars, doing integer multiplication
    P = (V * (255 - S)) >> 8
    Q = (V * (255 - ((S * remainder) >> 8))) >> 8
    T = (V * (255 - ((S * (255 - remainder)) >> 8))) >> 8


    # Assign temp vars based on color cone region
    if region == 0:
        R = V
        G = T
        B = P

    elif region == 1:
        R = Q
        G = V
        B = P

    elif region == 2:
        R = P
        G = V
        B = T

    elif region == 3:
        R = P
        G = Q
        B = V

    elif region == 4:
        R = T
        G = P
        B = V

    else:
        R = V
        G = P
        B = Q


    return (R, G, B)

def test_color(h, s, b):
    print('input colors', h, s, b)
    #print('colorsys convert', colorsys.hsv_to_rgb(h, s, b))
    print('hsb2rgb convert', hsb2rgb([h, s, b]))
    print('hsv_to_rgb convert', hsv_to_rgb(h, s, b))
    print('HSV_2_RGB convert', HSV_2_RGB([int(h), int(s), int(b)]))
    print('')

test_color(240.0, 1.0*100, 1.0*100)
test_color(359.00, 1.0000, 1.0000)
test_color(60.00, 1.0000, 1.0000)
test_color(240, 1, 1)