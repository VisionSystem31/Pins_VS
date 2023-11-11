
import Jetson.GPIO as GPIO
import os 
Salida = 11
energy_cut = 13

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(energy_cut, GPIO.IN)

if GPIO.input(energy_cut):
            cap.release()
            cv2.destroyAllWindows()
            GPIO.cleanup
            os.system("sudo shutdown -h now")




def turn_off_action():
    result = messagebox.askquestion("Confirmar apagado", "Seguro quiere apagar el sistema de vision?", icon='warning')
    if result == 'yes':    
        variables.Shut_down[0] = 1
        os.system("sudo shutdown -h now")
        root.destroy()

