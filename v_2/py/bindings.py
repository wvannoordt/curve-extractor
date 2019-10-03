from init_params import *
import tkinter.filedialog as tk_filedialog
import tkinter as tk
import numpy as np
import PIL.Image as pil_image
import PIL.ImageTk as pil_imagetk
from scipy import interpolate
import os


class Bindings:

    def __init__(self, underlying_window):
        self.window = underlying_window
        self.data = Params()
        self.make_bindings()
        self.init_entry_values()
        
    def init_entry_values(self):
        self.window.x1_entry.insert(0, "0")
        self.window.x2_entry.insert(0, "1")
        self.window.y1_entry.insert(0, "0")
        self.window.y2_entry.insert(0, "1")
        self.window.num_points_entry.insert(0, "100")
        
    def make_bindings(self):
    
        self.window.export_button.configure(command=self.export_data)
        self.window.export_button.configure(state="disabled")
        
        self.window.open_file_button.configure(command=self.open_image_file)
        
        self.window.x1_button.configure(command=self.on_x1_press)
        self.window.x2_button.configure(command=self.on_x2_press)
        self.window.y1_button.configure(command=self.on_y1_press)
        self.window.y2_button.configure(command=self.on_y2_press)
        
        self.window.image_canvas.bind("<Motion>", self.on_mouse_move)
        self.window.image_canvas.bind("<B3-Motion>", self.on_mouse3_drag_img)
        self.window.image_canvas.bind("<B1-Motion>", self.on_mouse1_drag_img)
        self.window.image_canvas.bind("<ButtonRelease-3>", self.on_b3_release_img)
        self.window.image_canvas.bind("<ButtonRelease-1>", self.on_b1_release_img)
        self.window.image_canvas.bind("<MouseWheel>", self.on_scroll_img)
        self.window.image_canvas.bind("<Button-1>", self.on_click_img)
        self.window.root.bind_all("<KeyPress>", self.key_press)
        self.window.root.bind_all("<KeyRelease>", self.key_release)
        self.window.x1_entry.bind("<FocusOut>", self.enforce_valid_entries)
        self.window.x2_entry.bind("<FocusOut>", self.enforce_valid_entries)
        self.window.y1_entry.bind("<FocusOut>", self.enforce_valid_entries)
        self.window.y2_entry.bind("<FocusOut>", self.enforce_valid_entries)
        self.window.num_points_entry.bind("<FocusOut>", self.enforce_valid_entries)
        
    def on_mouse_move(self, event):
        if self.any_select():
            if self.data.setting_x1:
                self.data.x1_pixel = (event.x - self.data.current_delta_x) / self.data.cur_ratio 
            if self.data.setting_x2:
                self.data.x2_pixel = (event.x - self.data.current_delta_x) / self.data.cur_ratio 
            if self.data.setting_y1:
                self.data.y1_pixel = (event.y - self.data.current_delta_y) / self.data.cur_ratio 
            if self.data.setting_y2:
                self.data.y2_pixel = (event.y - self.data.current_delta_y) / self.data.cur_ratio 
            self.refresh_all()
    
    def get_horizontal(self):
        return self.data.setting_y1 or self.data.setting_y2
    
    def any_select(self):
        return self.data.setting_x1 or self.data.setting_x2 or self.data.setting_y1 or self.data.setting_y2
    
    def enforce_valid_entries(self, event):
        try:
            self.data.x1_real = float(self.window.x1_entry.get())
        except ValueError:
            self.window.x1_entry.delete(0, tk.END)
            self.window.x1_entry.insert(0, str(self.data.x1_real))
        try:
            self.data.x2_real = float(self.window.x2_entry.get())
        except ValueError:
            self.window.x2_entry.delete(0, tk.END)
            self.window.x2_entry.insert(0, str(self.data.x2_real))
        try:
            self.data.y1_real = float(self.window.y1_entry.get())
        except ValueError:
            self.window.y1_entry.delete(0, tk.END)
            self.window.y1_entry.insert(0, str(self.data.y1_real))
        try:
            self.data.y2_real = float(self.window.y2_entry.get())
        except ValueError:
            self.window.y2_entry.delete(0, tk.END)
            self.window.y2_entry.insert(0, str(self.data.y2_real))
        try:
            ct = int(self.window.num_points_entry.get())
            if ct < 2:
                raise ValueError
            else:
                self.data.interp_points = ct
        except ValueError:
            self.window.num_points_entry.delete(0, tk.END)
            self.window.num_points_entry.insert(0, str(self.data.interp_points))
        self.refresh_all()
    
    def on_x1_press(self):
        if self.data.has_image:
            self.window.x1_button.config(relief=tk.SUNKEN)
            self.set_setting_var("x1")
    
    def on_x2_press(self):
        if self.data.has_image:
            self.window.x2_button.config(relief=tk.SUNKEN)
            self.set_setting_var("x2")
        
    def on_y1_press(self):
        if self.data.has_image:
            self.window.y1_button.config(relief=tk.SUNKEN)
            self.set_setting_var("y1")
        
    def on_y2_press(self):
        if self.data.has_image:
            self.window.y2_button.config(relief=tk.SUNKEN)
            self.set_setting_var("y2")
        
    def set_setting_var(self, str_set):
        self.data.setting_x1 = False
        self.data.setting_x2 = False
        self.data.setting_y1 = False
        self.data.setting_y2 = False
        if str_set == "x1":
            self.data.setting_x1 = True
        if str_set == "x2":
            self.data.setting_x2 = True
        if str_set == "y1":
            self.data.setting_y1 = True
        if str_set == "y2":
            self.data.setting_y2 = True
    
    def key_press(self, event):
        if event.keysym == "Control_L":
             self.data.controldown = True
        if event.keysym == "Delete":
            self.on_delete()
        if str(event.char) == "i":
            self.run_insert()
            
    def run_insert(self):
        if self.data.selected_index >= 0:
            n = len(self.data.profile_points)
            idx = self.get_idx_nearest_selected()
            pre = idx - 1
            post = idx + 1
            if pre < 0:
                pre = pre + n
            if post >= n:
                post = post - n
            target = idx
            if self.euc_dist(self.data.profile_points[self.data.selected_index], self.data.profile_points[pre]) > self.euc_dist(self.data.profile_points[self.data.selected_index], self.data.profile_points[post]):
                target = post
            self.data.profile_points.insert(target, self.data.profile_points[self.data.selected_index])
            del self.data.profile_points[self.data.selected_index + 1]
            self.data.selected_index = -1
            self.refresh_all()
            
    def euc_dist(self, a, b):
        return np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)  
            
    def get_idx_nearest_selected(self):
        cur_index = 0
        m_index = -1
        min_dist = 1e30
        cpt = self.data.profile_points[self.data.selected_index]
        for x in self.data.profile_points:
            if np.sqrt((x[0] - cpt[0])**2 + (x[1] - cpt[1])**2) < min_dist and not cur_index == self.data.selected_index:
                min_dist = np.sqrt((x[0] - cpt[0])**2 + (x[1] - cpt[1])**2)
                m_index = cur_index
            cur_index = cur_index + 1
        return m_index
            
    def on_delete(self):
        if self.data.selected_index >= 0:
            del self.data.profile_points[self.data.selected_index]
            self.data.selected_index = -1
            self.refresh_all()
        
    def key_release(self, event):
        if event.keysym == "Control_L":
             self.data.controldown = False
    
    def export_data(self):
        unit_per_pixel_x = (self.data.x2_real - self.data.x1_real) / (self.data.x2_pixel - self.data.x1_pixel)
        unit_per_pixel_y = (self.data.y2_real - self.data.y1_real) / (self.data.y2_pixel - self.data.y1_pixel)
        output_file = tk_filedialog.asksaveasfile(mode='w', defaultextension=".csv", filetypes = (("CSV","*.csv"),("Other","*")))
        n = len(self.data.x_data_points_px)
        for i in range(n):
            curx = self.data.x1_real + (self.data.x_data_points_px[i] - self.data.x1_pixel) * unit_per_pixel_x
            cury = self.data.y1_real + (self.data.y_data_points_px[i] - self.data.y1_pixel) * unit_per_pixel_y
            output_file.write("{},{}".format(curx, cury))
            output_file.write("\n")
        output_file.close()
        
    def on_click_img(self, event):
        pixel_x = (event.x - self.data.current_delta_x)/self.data.cur_ratio
        pixel_y = (event.y - self.data.current_delta_y)/self.data.cur_ratio
        if self.data.has_image and not self.any_select():
            if not self.data.controldown:
                if self.data.selected_index < 0:
                    min_dist = 1e-8
                    no_add_draw = False
                    for x in self.data.profile_points:
                        no_add_draw = np.sqrt((x[0] - pixel_x)**2 + (x[1] - pixel_y)**2) < min_dist or no_add_draw
                    if not no_add_draw:
                        self.data.profile_points.append((pixel_x, pixel_y))
                        self.draw_marker(pixel_x, pixel_y, False)
                self.refresh_all()
            else:
                self.determine_selection(pixel_x, pixel_y)
                self.refresh_all()
        self.data.setting_x1 = False
        self.data.setting_x2 = False
        self.data.setting_y1 = False
        self.data.setting_y2 = False
        self.window.x1_button.config(relief="flat")
        self.window.x2_button.config(relief="flat")
        self.window.y1_button.config(relief="flat")
        self.window.y2_button.config(relief="flat")
        
    def make_draw_spline(self):
        n = len(self.data.profile_points)
        if n > 3:
            self.data.has_exportable_spline = self.has_coordinate_sys()
            option = "disabled"
            if self.data.has_exportable_spline:
                option = "normal"
            self.window.export_button.config(state=option)
            x = []
            y = []
            for i in range(n):
                cpt = self.data.profile_points[i]
                x.append(cpt[0])
                y.append(cpt[1])
            points = [x, y]
            tck, u = interpolate.splprep(points, s=0)
            n = self.data.interp_points
            unew = np.arange(0, 1 + 1/n, 1/n)
            out = interpolate.splev(unew, tck)
            out_x = out[0]
            out_y = out[1]
            self.data.x_data_points_px = out_x
            self.data.y_data_points_px = out_y
            n_sm = len(out_x)
            for j in range(n_sm - 1):
                cx1 = self.data.cur_ratio * out_x[j] + self.data.current_delta_x
                cy1 = self.data.cur_ratio * out_y[j] + self.data.current_delta_y
                cx2 = self.data.cur_ratio * out_x[j+1] + self.data.current_delta_x
                cy2 = self.data.cur_ratio * out_y[j+1] + self.data.current_delta_y
                self.window.image_canvas.create_line(cx1, cy1, cx2, cy2, width=self.data.spline_width, fill="green")
        else:
            self.data.has_exportable_spline = False
            self.window.export_button.config(state="disabled")
    
    def has_coordinate_sys(self):
        return self.data.x1_pixel >= 0 and self.data.x2_pixel >= 0 and self.data.y1_pixel >= 0 and self.data.y2_pixel >= 0
    
    def refresh_all(self):
        if self.data.has_image:
            self.window.image_canvas.delete("all")
            photo = self.image_on_canvas
            self.curimg = self.window.image_canvas.create_image(0, 0, image=photo, anchor="nw")
            self.window.image_canvas.itemconfig(self.image_on_canvas, image = photo)
            self.window.image_canvas.move(self.curimg, self.data.current_delta_x, self.data.current_delta_y)
            self.draw_datum_lines(self.any_select())
            self.make_draw_spline()
            for x in self.data.profile_points:
                self.draw_marker(x[0], x[1], False)
            if self.data.selected_index >= 0:
                selected_pt = self.data.profile_points[self.data.selected_index]
                self.draw_marker(selected_pt[0], selected_pt[1], True)
                
    def draw_datum_lines(self, solid):
        if self.data.x1_pixel >= 0:
            curx1 = self.data.cur_ratio * self.data.x1_pixel + self.data.current_delta_x
            self.draw_vline(curx1, solid)
            self.window.image_canvas.create_text(int(curx1 + 0.5*self.data.typical_border), int(0.5*self.data.typical_border), fill="blue",font="Arial 10",text=("x1="+self.window.x1_entry.get()), anchor="nw")
        if self.data.x2_pixel >= 0:
            curx2 = self.data.cur_ratio * self.data.x2_pixel + self.data.current_delta_x
            self.draw_vline(curx2, solid)
            self.window.image_canvas.create_text(int(curx2 + 0.5*self.data.typical_border), int(0.5*self.data.typical_border),fill="blue",font="Arial 10",text=("x2="+self.window.x2_entry.get()), anchor="nw")
        if self.data.y1_pixel >= 0:
            cury1 = self.data.cur_ratio * self.data.y1_pixel + self.data.current_delta_y
            self.draw_hline(cury1, solid)
            self.window.image_canvas.create_text(int(0.5*self.data.typical_border), int(cury1 + 0.5*self.data.typical_border),fill="blue",font="Arial 10",text=("y1="+self.window.y1_entry.get()), anchor="nw")
        if self.data.y2_pixel >= 0:
            cury2 = self.data.cur_ratio * self.data.y2_pixel + self.data.current_delta_y
            self.window.image_canvas.create_text(int(0.5*self.data.typical_border), int(cury2 + 0.5*self.data.typical_border),fill="blue",font="Arial 10",text=("y2="+self.window.y2_entry.get()), anchor="nw")
            self.draw_hline(cury2, solid)
            
    def draw_vline(self, x, solid):
        if solid:
            self.window.image_canvas.create_line(int(x), 0, int(x), self.window.image_canvas.winfo_height())
        else:
            self.window.image_canvas.create_line(int(x), 0, int(x), self.window.image_canvas.winfo_height(), dash=(4, 2))
        
    def draw_hline(self, y, solid):
        if solid:
            self.window.image_canvas.create_line(0, int(y), self.window.image_canvas.winfo_width(), int(y))
        else:
            self.window.image_canvas.create_line(0, int(y), self.window.image_canvas.winfo_width(), int(y), dash=(4, 2))
        
    def determine_selection(self, xin, yin):
        min_index = -1
        min_distance = 1e30
        cur_index = 0
        for x in self.data.profile_points:
            current_distance = np.sqrt((x[0] - xin)**2 + (x[1] - yin)**2)
            if current_distance < min_distance:
                min_distance = current_distance
                min_index = cur_index
            cur_index = cur_index + 1
        if (min_distance / self.data.cur_ratio) < self.data.select_tolerance:
            self.data.selected_index = min_index
    
    def draw_marker(self, xin, yin, selected):
        x = (xin) * self.data.cur_ratio + self.data.current_delta_x
        y = (yin) * self.data.cur_ratio + self.data.current_delta_y
        if not selected:
            v = self.window.image_canvas.create_line(int(x), int(y - self.data.datum_marker_length), int(x), int(y + self.data.datum_marker_length), width = self.data.markerwidth)
            h = self.window.image_canvas.create_line(int(x - self.data.datum_marker_length), int(y), int(x + self.data.datum_marker_length), int(y), width = self.data.markerwidth)
        else:
            v = self.window.image_canvas.create_line(int(x), int(y - self.data.datum_marker_length), int(x), int(y + self.data.datum_marker_length), width = self.data.markerwidth, fill = "red")
            h = self.window.image_canvas.create_line(int(x - self.data.datum_marker_length), int(y), int(x + self.data.datum_marker_length), int(y), width = self.data.markerwidth, fill = "red")
        
    def on_b3_release_img(self, event):
        self.data.ini_m_x = -1
        self.data.ini_m_y = -1
    
    def on_b1_release_img(self, event):
        if not self.data.controldown:
            self.data.selected_index = -1
        self.refresh_all()
        self.data.ini_m_x_sel = -1
        self.data.ini_m_y_sel = -1
        
    def on_scroll_img(self, event):
        if self.data.has_image:
            sign_var = -1
            if sign_var*event.delta < 0:
                self.data.cur_ratio = self.data.cur_ratio * self.data.scroll_ratio
            else:
                self.data.cur_ratio = self.data.cur_ratio / self.data.scroll_ratio
            self.window.image_canvas.delete("all")
            new_height = int(self.data.cur_ratio * self.raw_image.height)
            new_width = int(self.data.cur_ratio * self.raw_image.width)
            image = self.raw_image.resize((new_width, new_height), pil_image.ANTIALIAS)
            photo = pil_imagetk.PhotoImage(image)
            photo.master = self.window.root
            self.image_on_canvas = photo
            self.curimg = self.window.image_canvas.create_image(0, 0, image=photo, anchor="nw")
            self.window.image_canvas.itemconfig(self.image_on_canvas, image = photo)
            self.window.image_canvas.move(self.curimg, self.data.current_delta_x, self.data.current_delta_y)
            self.refresh_all()
        
    def on_mouse1_drag_img(self, event):
        if self.data.has_image and self.data.selected_index >= 0:
            if self.data.ini_m_x_sel < 0:
                self.data.ini_m_x_sel = event.x
            if self.data.ini_m_y_sel < 0:
                self.data.ini_m_y_sel = event.y
            cx = event.x
            cy = event.y
            c_dx = cx - self.data.ini_m_x_sel;
            c_dy = cy - self.data.ini_m_y_sel;
            current_node = self.data.profile_points[self.data.selected_index]
            self.data.profile_points[self.data.selected_index] = (current_node[0] + c_dx / self.data.cur_ratio, current_node[1] + c_dy / self.data.cur_ratio)
            self.data.ini_m_x_sel = cx
            self.data.ini_m_y_sel = cy
            self.refresh_all()
    
    def on_mouse3_drag_img(self, event):
        if self.data.has_image:
            if self.data.ini_m_x < 0:
                self.data.ini_m_x = event.x
            if self.data.ini_m_y < 0:
                self.data.ini_m_y = event.y
            self.window.image_canvas.delete("all")
            photo = self.image_on_canvas
            self.curimg = self.window.image_canvas.create_image(0, 0, image=photo, anchor="nw")
            self.window.image_canvas.itemconfig(self.image_on_canvas, image = photo)
            cx = event.x
            cy = event.y
            self.window.image_canvas.move(self.curimg, self.data.current_delta_x, self.data.current_delta_y)
            self.data.current_delta_x = self.data.current_delta_x + cx - self.data.ini_m_x
            self.data.current_delta_y = self.data.current_delta_y + cy - self.data.ini_m_y
            self.data.ini_m_x = cx
            self.data.ini_m_y = cy
            self.refresh_all()
        
    def open_image_file(self):
        self.current_image_filename = tk_filedialog.askopenfilename(initialdir = ".",title = "Select file", filetypes = (("Images","*.jpg *.png"),("All files","*")))
        if (os.path.isfile(self.current_image_filename)):
            image = pil_image.open(self.current_image_filename)
            self.raw_image = image
            photo = pil_imagetk.PhotoImage(image)
            photo.master = self.window.root
            self.image_on_canvas = photo
            self.curimg = self.window.image_canvas.create_image(0, 0, image=photo, anchor="nw")
            self.window.image_canvas.itemconfig(self.image_on_canvas, image = photo)
            self.data.has_image = True
