
import struct
import zlib
import pygame
import os

class AsepriteReader:
    def __init__(self, filename):
        self.filename = filename
        self.frames = [] # List of (surface, duration)
        self.width = 0
        self.height = 0
        self.color_depth = 0
        self.palette = [] # List of (r,g,b,a)
        
        if not os.path.exists(filename):
            print(f"Error: File {filename} not found.")
            return

        try:
            self.load()
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            import traceback
            traceback.print_exc()

    def load(self):
        with open(self.filename, 'rb') as f:
            # Main Header (128 bytes)
            header_data = f.read(128)
            if len(header_data) < 128:
                print("Header too short")
                return

            # DWORD File size
            filesize = struct.unpack('<I', header_data[0:4])[0]
            
            # Magic number rip
            magic = struct.unpack('<H', header_data[4:6])[0]
            if magic != 0xA5E0:
                print(f"Invalid magic: {hex(magic)}")
                return
                
   
            frames_count = struct.unpack('<H', header_data[6:8])[0]
            
            self.width = struct.unpack('<H', header_data[8:10])[0]
            
            self.height = struct.unpack('<H', header_data[10:12])[0]
            
            self.color_depth = struct.unpack('<H', header_data[12:14])[0]
            
            flags = struct.unpack('<I', header_data[14:18])[0]
            

            self.transparent_index = header_data[28]
                        
            # Loop to read the frames
            for i in range(frames_count):
                self.read_frame(f)

    def read_frame(self, f):
        frame_header = f.read(16)
        if len(frame_header) < 16:
            return

        bytes_in_frame = struct.unpack('<I', frame_header[0:4])[0]
        
        magic = struct.unpack('<H', frame_header[4:6])[0]
        if magic != 0xF1FA:
            print(f"Invalid frame magic: {hex(magic)}")

            return

        old_chunk_count = struct.unpack('<H', frame_header[6:8])[0]
        duration = struct.unpack('<H', frame_header[8:10])[0]
        
        chunk_count = old_chunk_count
        if old_chunk_count == 0xFFFF:
             chunk_count = struct.unpack('<I', frame_header[12:16])[0]

        data_len = bytes_in_frame - 16
        chunks_data = f.read(data_len)
        
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        surface.fill((0,0,0,0))
        
        offset = 0
        for _ in range(chunk_count):
            if offset + 6 > len(chunks_data):
                break
            
            chunk_size = struct.unpack('<I', chunks_data[offset:offset+4])[0]
            chunk_type = struct.unpack('<H', chunks_data[offset+4:offset+6])[0]
            
            # Chunk data starts at offset+6, length is chunk_size-6
            chunk_content = chunks_data[offset+6 : offset+chunk_size]
            
            self.process_chunk(chunk_type, chunk_content, surface)
            
            offset += chunk_size
            
        self.frames.append(surface)

    def process_chunk(self, chunk_type, data, surface):
        
        if chunk_type == 0x2005: # Cel
            self.process_cel(data, surface)
        elif chunk_type == 0x2019: # Palette
            self.process_palette(data)

    def process_palette(self, data):
        
        first_index = struct.unpack('<I', data[4:8])[0]
        last_index = struct.unpack('<I', data[8:12])[0]
        count = last_index - first_index + 1
        
        off = 20 # 4+4+4+8
        
        while len(self.palette) <= last_index:
            self.palette.append((0,0,0,0))
            
        current = first_index
        for _ in range(count):

            flags = struct.unpack('<H', data[off:off+2])[0]
            r = data[off+2]
            g = data[off+3]
            b = data[off+4]
            a = data[off+5]
            off += 6
            
            if flags & 1:

                name_len = struct.unpack('<H', data[off:off+2])[0]
                off += 2 + name_len
            
            self.palette[current] = (r, g, b, a)
            current += 1

    def process_cel(self, data, surface):
        layer_index = struct.unpack('<H', data[0:2])[0]
        x = struct.unpack('<h', data[2:4])[0]
        y = struct.unpack('<h', data[4:6])[0]
        opacity = data[6]
        cel_type = struct.unpack('<H', data[7:9])[0]
        
        pixel_data = data[16:]
        
        width = 0
        height = 0
        raw_image = None
        
        if cel_type == 0: # Raw
            width = struct.unpack('<H', pixel_data[0:2])[0]
            height = struct.unpack('<H', pixel_data[2:4])[0]
            raw_image = pixel_data[4:]
            
        elif cel_type == 1: # Linked
            return # stop
            
        elif cel_type == 2: 
            width = struct.unpack('<H', pixel_data[0:2])[0]
            height = struct.unpack('<H', pixel_data[2:4])[0]
            try:
                raw_image = zlib.decompress(pixel_data[4:])
            except Exception as e:
                print(f"Zlib error: {e}")
                return
        
        if raw_image is None:
            return

        self.draw_cel_pixels(surface, raw_image, x, y, width, height, opacity)

    def draw_cel_pixels(self, surface, raw, x, y, w, h, opacity):
        cel_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        
        if self.color_depth == 32:
            try:
                img = pygame.image.frombytes(raw, (w, h), "RGBA")
                surface.blit(img, (x, y))
            except Exception as e:
                print(f"Error creating RGBA image: {e}")
                
        elif self.color_depth == 8: # Indexed

            rgba = bytearray(w * h * 4)
            idx_ptr = 0
            rgba_ptr = 0
            
            pal_len = len(self.palette)
            
            
            for i in range(w*h):
                color_idx = raw[i]
                
                if color_idx == self.transparent_index:

                    r,g,b,a = 0,0,0,0
                elif color_idx < pal_len:
                    r,g,b,a = self.palette[color_idx]
                else:
                    r,g,b,a = 0,0,0,255 
                
                rgba[i*4] = r
                rgba[i*4+1] = g
                rgba[i*4+2] = b
                rgba[i*4+3] = a
            
            img = pygame.image.frombytes(bytes(rgba), (w, h), "RGBA")
            surface.blit(img, (x, y))
        
        elif self.color_depth == 16: # Grayscale
            # TODO
            pass
