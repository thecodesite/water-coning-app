import numpy as np
import math
def meyer_gardner(ko, h, hp, mu, Bo, re, rw, Deno, Denw):
    return (0.0000246 * ((Denw - Deno) / (np.log(re / rw)))) * (ko / (mu * Bo)) * ((pow((h), 2)) - (pow((hp), 2)))

def chaperson(kh, kv, h, hp, mu, Bo, Denw, Deno, re):
    return (0.00000783 * (kh * pow((h - hp), 2) / (mu * Bo)) * (Denw - Deno)) * ((0.7311 + (1.943 / ((re / h) * math.sqrt(kv / kh)))))

def schols(ko, h, hp, mu, rw, re, Denw, Deno, Bo):
    return (0.00000783 * (Denw - Deno) * ko * ((pow((h), 2)) - (pow((hp), 2))) / (mu * Bo) * (0.432 + 3.142 / (np.log(re / rw))) * (pow(h / re, 0.14)))

def muskat_wyckoff(ko, h, hp, mu, re, Denw, Deno, Bo, rw):
    return (0.0000924 * (((Denw - Deno) * ko) * (pow((1 - (pow((hp / h), 2))), 1.325)) / (mu * Bo)) * (pow(h, 2.238)) * pow((np.log(re / rw)), -1.99))

def sobocinski_cornelius(kh, h, hp, mu, rw, re, Denw, Deno, Bo, Qo, kro, krw, mw, phi):
    Z = 0.0000492 * (Denw - Deno) * kh * h * (h - hp) / (mu * Bo * Qo)
    TDbt = (4 * Z + pow(Z, 2) - 0.75 * pow(Z, 3)) / (7 - 2 * Z)
    M = (krw / kro) * (mu / mw)
    
    if M <= 1:
        alfa = 0.5
    else:
        alfa = 0.6
    
    Tbt = (20325 * mu * h * phi * TDbt) / ((Denw - Deno) * kv * (1 + pow(M, alfa)))
    Qoc_sobocinski_cornelius = 0.0000141 * ((Denw - Deno) * kh * h * (h - hp)) / (mu * Bo)

    return Tbt, Qoc_sobocinski_cornelius
