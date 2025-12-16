import requests
import time
import random
import click

from sense_hat import SenseHat
sense = SenseHat()

def keyboard_get_direction():
    d_longitude, d_latitude = 0, 0
    send_velocity = True
    click = click.getchar()
    match click:
        case 'a':
            click.echo('Left')
            d_longitude, d_latitude = -1, 0
            
        case 'd':
            click.echo('Right')
            d_longitude, d_latitude = 1, 0
            
        case 'w':
            click.echo('Up')
            d_longitude, d_latitude = 0, 1
            
        case 's':
            click.echo('Down')
            d_longitude, d_latitude = 0, -1
            
        case _:
            send_velocity = False
            click.echo('Invalid input :(')
    return d_longitude, d_latitude, send_velocity

def sensehat_get_direction():
    d_longitude, d_latitude = 0, 0
    send_velocity = True
    event = sense.stick.get_events()
    if len(event) != 0:
        match event[len(event) - 1].direction:
            case 'left':
                click.echo('Left')
                d_longitude, d_latitude = -1, 0
                    
            case 'right':
                click.echo('Right')
                d_longitude, d_latitude = 1, 0
                    
            case 'up':
                click.echo('Up')
                d_longitude, d_latitude = 0, 1
                    
            case 'down':
                click.echo('Down')
                d_longitude, d_latitude = 0, -1
                    
            case _:
                send_velocity = False
                    
    return d_longitude, d_latitude, send_velocity

if __name__ == "__main__":
    SERVER_URL = "http://127.0.0.1:5000/drone"
    while True:
        d_longitude, d_latitude, send_velocity = sensehat_get_direction()
        if send_velocity:
            with requests.Session() as session:
                current_location = {'longitude': d_longitude,
                                    'latitude': d_latitude
                                    }
                resp = session.post(SERVER_URL, json=current_location)
