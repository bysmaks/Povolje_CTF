#!/bin/sh
socat tcp-listen:6969,reuseaddr,fork exec:"./zamena"

