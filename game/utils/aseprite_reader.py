
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
            
            # WORD Magic number (0xA5E0)
            magic = struct.unpack('<H', header_data[4:6])[0]
            if magic != 0xA5E0:
                print(f"Invalid magic: {hex(magic)}")
                return
                
            # WORD Frames
            frames_count = struct.unpack('<H', header_data[6:8])[0]
            
            # WORD Width
            self.width = struct.unpack('<H', header_data[8:10])[0]
            
            # WORD Height
            self.height = struct.unpack('<H', header_data[10:12])[0]
            
            # WORD Color depth (bpp)
            self.color_depth = struct.unpack('<H', header_data[12:14])[0]
            
            # DWORD Flags
            flags = struct.unpack('<I', header_data[14:18])[0]
            
            # WORD Speed (DEPRECATED)
            # DWORD 0
            # DWORD 0
            # BYTE Palette entry (transparent index)
            self.transparent_index = header_data[28]
            
            # Ignore rest 
            
            # Loop frames
            for i in range(frames_count):
                self.read_frame(f)

    def read_frame(self, f):
        # Frame Header (16 bytes)
        frame_header = f.read(16)
        if len(frame_header) < 16:
            return

        bytes_in_frame = struct.unpack('<I', frame_header[0:4])[0]
        
        # WORD Magic number (0xF1FA)
        magic = struct.unpack('<H', frame_header[4:6])[0]
        if magic != 0xF1FA:
            print(f"Invalid frame magic: {hex(magic)}")
            # Skip invalid frame data to try to recover?
            # Or just stop?
            return

        old_chunk_count = struct.unpack('<H', frame_header[6:8])[0]
        duration = struct.unpack('<H', frame_header[8:10])[0]
        
        # New chunk count at offset 12? 
        # Actually bytes 12-16 are reserved/new chunk count if old is FFFF
        chunk_count = old_chunk_count
        if old_chunk_count == 0xFFFF:
             chunk_count = struct.unpack('<I', frame_header[12:16])[0]

        # Read the chunks data for this frame
        # bytes_in_frame includes the 16 bytes header
        data_len = bytes_in_frame - 16
        chunks_data = f.read(data_len)
        
        # Create surface for this frame
        # For RGBA (32bpp) or Indexed (8bpp) converted
        # Always use RGBA surface for Pygame
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # Clear with transparent
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
        # 0x0004: Old Palette 1
        # 0x0011: Old Palette 2
        # 0x2004: Layer
        # 0x2005: Cel
        # 0x2006: Cel Extra
        # 0x2019: Palette
        
        if chunk_type == 0x2005: # Cel
            self.process_cel(data, surface)
        elif chunk_type == 0x2019: # Palette
            self.process_palette(data)

    def process_palette(self, data):
        # DWORD Size (palette size)
        # DWORD First
        # DWORD Last
        # BYTE[8] Reserved
        
        first_index = struct.unpack('<I', data[4:8])[0]
        last_index = struct.unpack('<I', data[8:12])[0]
        count = last_index - first_index + 1
        
        off = 20 # 4+4+4+8
        
        # We need to expand palette list if needed
        # Assuming max 256 colors for 8bpp
        while len(self.palette) <= last_index:
            self.palette.append((0,0,0,0))
            
        current = first_index
        for _ in range(count):
            # WORD Flags (1=HasName)
            flags = struct.unpack('<H', data[off:off+2])[0]
            r = data[off+2]
            g = data[off+3]
            b = data[off+4]
            a = data[off+5]
            off += 6
            
            if flags & 1:
                # WORD Name Len
                name_len = struct.unpack('<H', data[off:off+2])[0]
                off += 2 + name_len
            
            self.palette[current] = (r, g, b, a)
            current += 1

    def process_cel(self, data, surface):
        # WORD Layer Index
        layer_index = struct.unpack('<H', data[0:2])[0]
        # SHORT X
        x = struct.unpack('<h', data[2:4])[0]
        # SHORT Y
        y = struct.unpack('<h', data[4:6])[0]
        # BYTE Opacity
        opacity = data[6]
        # WORD Cel Type
        cel_type = struct.unpack('<H', data[7:9])[0]
        # BYTE[7] Reserved
        
        # Pixel data starts at 16
        pixel_data = data[16:]
        
        width = 0
        height = 0
        raw_image = None
        
        if cel_type == 0: # Raw
            width = struct.unpack('<H', pixel_data[0:2])[0]
            height = struct.unpack('<H', pixel_data[2:4])[0]
            raw_image = pixel_data[4:]
            
        elif cel_type == 1: # Linked
            # WORD Frame position
            return # Ignore linked for now, needs tracking of previous frames
            
        elif cel_type == 2: # Compressed Image
            width = struct.unpack('<H', pixel_data[0:2])[0]
            height = struct.unpack('<H', pixel_data[2:4])[0]
            try:
                raw_image = zlib.decompress(pixel_data[4:])
            except Exception as e:
                print(f"Zlib error: {e}")
                return
        
        if raw_image is None:
            return

        # Draw to surface
        self.draw_cel_pixels(surface, raw_image, x, y, width, height, opacity)

    def draw_cel_pixels(self, surface, raw, x, y, w, h, opacity):
        # Create a temporary surface for the cel
        # We need to handle bpp
        cel_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        
        # If 32 bpp (RGBA)
        if self.color_depth == 32:
            try:
                # Aseprite RGBA is straight forward
                img = pygame.image.frombytes(raw, (w, h), "RGBA")
                # Apply opacity?
                # Ideally per pixel, but blit supports alpha
                surface.blit(img, (x, y))
            except Exception as e:
                print(f"Error creating RGBA image: {e}")
                
        elif self.color_depth == 8: # Indexed
            # Manual conversion using palette
            # Fast enough for small sprites?
            # Or use numpy/surfarray if available? pure python for now.
            
            # Construct RGBA buffer
            rgba = bytearray(w * h * 4)
            idx_ptr = 0
            rgba_ptr = 0
            
            pal_len = len(self.palette)
            
            # Optimization: Pre-lookup
            
            for i in range(w*h):
                color_idx = raw[i]
                
                if color_idx == self.transparent_index:
                    # Transparent
                    r,g,b,a = 0,0,0,0
                elif color_idx < pal_len:
                    r,g,b,a = self.palette[color_idx]
                else:
                    r,g,b,a = 0,0,0,255 # Fallback black?
                
                # Apply global opacity
                # a = (a * opacity) // 255
                
                rgba[i*4] = r
                rgba[i*4+1] = g
                rgba[i*4+2] = b
                rgba[i*4+3] = a
            
            img = pygame.image.frombytes(bytes(rgba), (w, h), "RGBA")
            surface.blit(img, (x, y))
        
        elif self.color_depth == 16: # Grayscale
            # TODO
            pass
