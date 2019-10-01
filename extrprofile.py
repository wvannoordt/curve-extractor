#Will van Noordt

import numpy as np
import tkinter as tk
import tkinter.filedialog as tk_filedialog
import PIL.Image as pil_image
import PIL.ImageTk as pil_imagetk
from scipy import interpolate
import os

class ProfileExtractWindow:

    def __init__(self):
        self.window_width = 1320
        self.window_height = 768
        self.master = tk.Tk()
        self.background_canvas =  tk.Canvas(self.master, width=self.window_width, height=self.window_height)
        self.background_canvas.pack()
        self.typical_border = 10
        self.workspace_width = 150
        self.ini_m_x = -1
        self.ini_m_y = -1
        self.ini_m_x_sel = -1
        self.ini_m_y_sel = -1
        self.scroll_ratio = 1.1
        self.cur_ratio = 1.0
        self.spline_width = 3
        self.current_delta_x = 0
        self.current_delta_y = 0
        self.has_image = False
        self.bottom_label_distance = 20
        self.datum_marker_length = 10
        self.datum_markers_image_coords = ((-1, -1), (-1, -1), (-1, -1), (-1, -1))
        self.profile_points = []
        self.markerwidth = 3
        self.controldown = False
        self.select_tolerance = 1.05 * self.datum_marker_length
        self.selected_index = -1
        self.datum_entry_width = 50
        self.label_disp = 5
        self.lb_width = 30
        self.x1_pixel = -1
        self.x2_pixel = -1
        self.y1_pixel = -1
        self.y2_pixel = -1
        self.x1_real = 0
        self.x2_real = 1
        self.y1_real = 0
        self.y2_real = 1
        self.setting_x1 = False
        self.setting_x2 = False
        self.setting_y1 = False
        self.setting_y2 = False
        self.im_canv_height = 700
        self.im_canv_width = 1000
        self.interp_points = 100
        self.has_exportable_spline = False
        self.x_data_points_px = ()
        self.y_data_points_px = ()
        
        self.init_gui_elements()
     
    def open_window(self):
        self.master.mainloop()
        
    def init_gui_elements(self):
        self.open_file_button = tk.Button(self.master, command=self.open_image_file, text="Open...")
        self.open_file_button.place(x=self.typical_border,y=self.typical_border)
        
        self.master.update()
        
        self.export_button = tk.Button(self.master, command=self.export_data, text="Export")
        self.export_button.place(x=2*self.typical_border + self.open_file_button.winfo_width(), y = self.typical_border)
        self.export_button.config(state="disabled")
        
        self.image_canvas = tk.Canvas(self.master, width=self.im_canv_width, height=self.im_canv_height, bd=2, bg="grey", highlightcolor="red")
        self.image_canvas.place(x = self.workspace_width + self.typical_border, y = self.typical_border)
        
        self.x1_button = tk.Button(self.master, command=self.on_x1_press, text="Place x1")
        self.x1_button.place(x = self.typical_border, y = self.open_file_button.winfo_height() + 2 * self.typical_border)
        
        self.master.update()
        
        self.x1_entry = tk.Entry(self.master)
        self.x1_entry.insert(0, "0")
        self.x1_entry.place(x = 2*self.typical_border + self.x1_button.winfo_width() + self.lb_width, y = self.open_file_button.winfo_height() + 2 * self.typical_border + self.label_disp, width=self.datum_entry_width)
        
        self.x1_label = tk.Label(self.master, text="x1=")
        self.x1_label.place(x = 2*self.typical_border + self.x1_button.winfo_width(), y = self.open_file_button.winfo_height() + 2 * self.typical_border + self.label_disp)
        
        self.x2_button = tk.Button(self.master, command=self.on_x2_press, text="Place x2")
        self.x2_button.place(x = self.typical_border, y = 2*self.open_file_button.winfo_height() + 3 * self.typical_border)
        
        self.x2_entry = tk.Entry(self.master)
        self.x2_entry.insert(0, "1.0")
        self.x2_entry.place(x = 2*self.typical_border + self.x1_button.winfo_width() + self.lb_width, y = 2*self.open_file_button.winfo_height() + 3 * self.typical_border + self.label_disp, width=self.datum_entry_width)
        
        self.x2_label = tk.Label(self.master, text="x2=")
        self.x2_label.place(x = 2*self.typical_border + self.x1_button.winfo_width(), y = 2*self.open_file_button.winfo_height() + 3 * self.typical_border + self.label_disp)
        
        self.y1_button = tk.Button(self.master, command=self.on_y1_press, text="Place y1")
        self.y1_button.place(x = self.typical_border, y = 3*self.open_file_button.winfo_height() + 4 * self.typical_border)
        
        self.y1_entry = tk.Entry(self.master)
        self.y1_entry.insert(0, "0")
        self.y1_entry.place(x = 2*self.typical_border + self.x1_button.winfo_width() + self.lb_width, y = 3*self.open_file_button.winfo_height() + 4 * self.typical_border + self.label_disp, width=self.datum_entry_width)
        
        self.y1_label = tk.Label(self.master, text="y1=")
        self.y1_label.place(x = 2*self.typical_border + self.x1_button.winfo_width(), y = 3*self.open_file_button.winfo_height() + 4 * self.typical_border + self.label_disp)
        
        self.y2_button = tk.Button(self.master, command=self.on_y2_press, text="Place y2")
        self.y2_button.place(x = self.typical_border, y = 4*self.open_file_button.winfo_height() + 5 * self.typical_border)
        
        self.y2_entry = tk.Entry(self.master)
        self.y2_entry.insert(0, "1.0")
        self.y2_entry.place(x = 2*self.typical_border + self.x1_button.winfo_width() + self.lb_width, y = 4*self.open_file_button.winfo_height() + 5 * self.typical_border + self.label_disp, width=self.datum_entry_width)
        
        self.y2_label = tk.Label(self.master, text="y2=")
        self.y2_label.place(x = 2*self.typical_border + self.x1_button.winfo_width(), y = 4*self.open_file_button.winfo_height() + 5 * self.typical_border + self.label_disp)
        
        self.num_points_entry = tk.Entry(self.master)
        self.num_points_entry.insert(0, str(self.interp_points))
        self.num_points_entry.place(x = 2*self.typical_border + 3*self.lb_width, y = 5*self.open_file_button.winfo_height() + 6 * self.typical_border, width=int(0.8*self.datum_entry_width))
        
        self.num_points_label = tk.Label(self.master, text="Number of points:")
        self.num_points_label.place(x = self.typical_border, y = 5*self.open_file_button.winfo_height() + 6 * self.typical_border)
        
        self.image_canvas.bind("<Motion>", self.on_mouse_move)
        self.image_canvas.bind("<B3-Motion>", self.on_mouse3_drag_img)
        self.image_canvas.bind("<B1-Motion>", self.on_mouse1_drag_img)
        self.image_canvas.bind("<ButtonRelease-3>", self.on_b3_release_img)
        self.image_canvas.bind("<ButtonRelease-1>", self.on_b1_release_img)
        self.image_canvas.bind("<MouseWheel>", self.on_scroll_img)
        self.image_canvas.bind("<Button-1>", self.on_click_img)
        self.master.bind_all("<KeyPress>", self.key_press)
        self.master.bind_all("<KeyRelease>", self.key_release)
        self.x1_entry.bind("<FocusOut>", self.enforce_valid_entries)
        self.x2_entry.bind("<FocusOut>", self.enforce_valid_entries)
        self.y1_entry.bind("<FocusOut>", self.enforce_valid_entries)
        self.y2_entry.bind("<FocusOut>", self.enforce_valid_entries)
        self.num_points_entry.bind("<FocusOut>", self.enforce_valid_entries)
        
        self.master.title("Profile Extractor")
    
    def on_mouse_move(self, event):
        if self.any_select():
            if self.setting_x1:
                self.x1_pixel = (event.x - self.current_delta_x) / self.cur_ratio 
            if self.setting_x2:
                self.x2_pixel = (event.x - self.current_delta_x) / self.cur_ratio 
            if self.setting_y1:
                self.y1_pixel = (event.y - self.current_delta_y) / self.cur_ratio 
            if self.setting_y2:
                self.y2_pixel = (event.y - self.current_delta_y) / self.cur_ratio 
            self.refresh_all()
    
    def get_horizontal(self):
        return self.setting_y1 or self.setting_y2
    
    def any_select(self):
        return self.setting_x1 or self.setting_x2 or self.setting_y1 or self.setting_y2
    
    def enforce_valid_entries(self, event):
        try:
            self.x1_real = float(self.x1_entry.get())
        except ValueError:
            self.x1_entry.delete(0, tk.END)
            self.x1_entry.insert(0, str(self.x1_real))
        try:
            self.x2_real = float(self.x2_entry.get())
        except ValueError:
            self.x2_entry.delete(0, tk.END)
            self.x2_entry.insert(0, str(self.x2_real))
        try:
            self.y1_real = float(self.y1_entry.get())
        except ValueError:
            self.y1_entry.delete(0, tk.END)
            self.y1_entry.insert(0, str(self.y1_real))
        try:
            self.y2_real = float(self.y2_entry.get())
        except ValueError:
            self.y2_entry.delete(0, tk.END)
            self.y2_entry.insert(0, str(self.y2_real))
        try:
            ct = int(self.num_points_entry.get())
            if ct < 2:
                raise ValueError
            else:
                self.interp_points = ct
        except ValueError:
            self.num_points_entry.delete(0, tk.END)
            self.num_points_entry.insert(0, str(self.interp_points))
        self.refresh_all()
    
    def on_x1_press(self):
        if self.has_image:
            self.x1_button.config(relief=tk.SUNKEN)
            self.set_setting_var("x1")
    
    def on_x2_press(self):
        if self.has_image:
            self.x2_button.config(relief=tk.SUNKEN)
            self.set_setting_var("x2")
        
    def on_y1_press(self):
        if self.has_image:
            self.y1_button.config(relief=tk.SUNKEN)
            self.set_setting_var("y1")
        
    def on_y2_press(self):
        if self.has_image:
            self.y2_button.config(relief=tk.SUNKEN)
            self.set_setting_var("y2")
        
    def set_setting_var(self, str_set):
        self.setting_x1 = False
        self.setting_x2 = False
        self.setting_y1 = False
        self.setting_y2 = False
        if str_set == "x1":
            self.setting_x1 = True
        if str_set == "x2":
            self.setting_x2 = True
        if str_set == "y1":
            self.setting_y1 = True
        if str_set == "y2":
            self.setting_y2 = True
    
    def key_press(self, event):
        if event.keysym == "Control_L":
             self.controldown = True
        if event.keysym == "Delete":
            self.on_delete()
        if str(event.char) == "i":
            self.run_insert()
            
    def run_insert(self):
        if self.selected_index >= 0:
            n = len(self.profile_points)
            idx = self.get_idx_nearest_selected()
            pre = idx - 1
            post = idx + 1
            if pre < 0:
                pre = pre + n
            if post >= n:
                post = post - n
            target = idx
            if self.euc_dist(self.profile_points[self.selected_index], self.profile_points[pre]) > self.euc_dist(self.profile_points[self.selected_index], self.profile_points[post]):
                target = post
            self.profile_points.insert(target, self.profile_points[self.selected_index])
            del self.profile_points[self.selected_index + 1]
            self.selected_index = -1
            self.refresh_all()
            
    def euc_dist(self, a, b):
        return np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)  
            
    def get_idx_nearest_selected(self):
        cur_index = 0
        m_index = -1
        min_dist = 1e30
        cpt = self.profile_points[self.selected_index]
        for x in self.profile_points:
            if np.sqrt((x[0] - cpt[0])**2 + (x[1] - cpt[1])**2) < min_dist and not cur_index == self.selected_index:
                min_dist = np.sqrt((x[0] - cpt[0])**2 + (x[1] - cpt[1])**2)
                m_index = cur_index
            cur_index = cur_index + 1
        return m_index
            
    def on_delete(self):
        if self.selected_index >= 0:
            del self.profile_points[self.selected_index]
            self.selected_index = -1
            self.refresh_all()
        
    def key_release(self, event):
        if event.keysym == "Control_L":
             self.controldown = False
    
    def export_data(self):
        unit_per_pixel_x = (self.x2_real - self.x1_real) / (self.x2_pixel - self.x1_pixel)
        unit_per_pixel_y = (self.y2_real - self.y1_real) / (self.y2_pixel - self.y1_pixel)
        output_file = tk_filedialog.asksaveasfile(mode='w', defaultextension=".csv", filetypes = (("CSV","*.csv"),("Other","*")))
        n = len(self.x_data_points_px)
        for i in range(n):
            curx = self.x1_real + (self.x_data_points_px[i] - self.x1_pixel) * unit_per_pixel_x
            cury = self.y1_real + (self.y_data_points_px[i] - self.y1_pixel) * unit_per_pixel_y
            output_file.write("{},{}".format(curx, cury))
            output_file.write("\n")
        output_file.close()
        
    def on_click_img(self, event):
        pixel_x = (event.x - self.current_delta_x)/self.cur_ratio
        pixel_y = (event.y - self.current_delta_y)/self.cur_ratio
        if self.has_image and not self.any_select():
            if not self.controldown:
                if self.selected_index < 0:
                    min_dist = 1e-8
                    no_add_draw = False
                    for x in self.profile_points:
                        no_add_draw = np.sqrt((x[0] - pixel_x)**2 + (x[1] - pixel_y)**2) < min_dist or no_add_draw
                    if not no_add_draw:
                        self.profile_points.append((pixel_x, pixel_y))
                        self.draw_marker(pixel_x, pixel_y, False)
                self.refresh_all()
            else:
                self.determine_selection(pixel_x, pixel_y)
                self.refresh_all()
        self.setting_x1 = False
        self.setting_x2 = False
        self.setting_y1 = False
        self.setting_y2 = False
        self.x1_button.config(relief=tk.RAISED)
        self.x2_button.config(relief=tk.RAISED)
        self.y1_button.config(relief=tk.RAISED)
        self.y2_button.config(relief=tk.RAISED)
        
    def make_draw_spline(self):
        n = len(self.profile_points)
        if n > 3:
            self.has_exportable_spline = self.has_coordinate_sys()
            option = "disabled"
            if self.has_exportable_spline:
                option = "normal"
            self.export_button.config(state=option)
            x = []
            y = []
            for i in range(n):
                cpt = self.profile_points[i]
                x.append(cpt[0])
                y.append(cpt[1])
            points = [x, y]
            tck, u = interpolate.splprep(points, s=0)
            n = self.interp_points
            unew = np.arange(0, 1 + 1/n, 1/n)
            out = interpolate.splev(unew, tck)
            out_x = out[0]
            out_y = out[1]
            self.x_data_points_px = out_x
            self.y_data_points_px = out_y
            n_sm = len(out_x)
            for j in range(n_sm - 1):
                cx1 = self.cur_ratio * out_x[j] + self.current_delta_x
                cy1 = self.cur_ratio * out_y[j] + self.current_delta_y
                cx2 = self.cur_ratio * out_x[j+1] + self.current_delta_x
                cy2 = self.cur_ratio * out_y[j+1] + self.current_delta_y
                self.image_canvas.create_line(cx1, cy1, cx2, cy2, width=self.spline_width, fill="green")
        else:
            self.has_exportable_spline = False
            self.export_button.config(state="disabled")
    
    def has_coordinate_sys(self):
        return self.x1_pixel >= 0 and self.x2_pixel >= 0 and self.y1_pixel >= 0 and self.y2_pixel >= 0
    
    def refresh_all(self):
        if self.has_image:
            self.image_canvas.delete("all")
            photo = self.image_on_canvas
            self.curimg = self.image_canvas.create_image(0, 0, image=photo, anchor="nw")
            self.image_canvas.itemconfig(self.image_on_canvas, image = photo)
            self.image_canvas.move(self.curimg, self.current_delta_x, self.current_delta_y)
            self.draw_datum_lines(self.any_select())
            self.make_draw_spline()
            for x in self.profile_points:
                self.draw_marker(x[0], x[1], False)
            if self.selected_index >= 0:
                selected_pt = self.profile_points[self.selected_index]
                self.draw_marker(selected_pt[0], selected_pt[1], True)
                
    def draw_datum_lines(self, solid):
        if self.x1_pixel >= 0:
            curx1 = self.cur_ratio * self.x1_pixel + self.current_delta_x
            self.draw_vline(curx1, solid)
            self.image_canvas.create_text(int(curx1 + 0.5*self.typical_border), int(0.5*self.typical_border), fill="darkblue",font="Arial 10",text=("x1="+self.x1_entry.get()), anchor="nw")
        if self.x2_pixel >= 0:
            curx2 = self.cur_ratio * self.x2_pixel + self.current_delta_x
            self.draw_vline(curx2, solid)
            self.image_canvas.create_text(int(curx2 + 0.5*self.typical_border), int(0.5*self.typical_border),fill="darkblue",font="Arial 10",text=("x2="+self.x2_entry.get()), anchor="nw")
        if self.y1_pixel >= 0:
            cury1 = self.cur_ratio * self.y1_pixel + self.current_delta_y
            self.draw_hline(cury1, solid)
            self.image_canvas.create_text(int(0.5*self.typical_border), int(cury1 + 0.5*self.typical_border),fill="darkblue",font="Arial 10",text=("y1="+self.y1_entry.get()), anchor="nw")
        if self.y2_pixel >= 0:
            cury2 = self.cur_ratio * self.y2_pixel + self.current_delta_y
            self.image_canvas.create_text(int(0.5*self.typical_border), int(cury2 + 0.5*self.typical_border),fill="darkblue",font="Arial 10",text=("y2="+self.y2_entry.get()), anchor="nw")
            self.draw_hline(cury2, solid)
            
    def draw_vline(self, x, solid):
        if solid:
            self.image_canvas.create_line(int(x), 0, int(x), self.im_canv_height)
        else:
            self.image_canvas.create_line(int(x), 0, int(x), self.im_canv_height, dash=(4, 2))
        
    def draw_hline(self, y, solid):
        if solid:
            self.image_canvas.create_line(0, int(y), self.im_canv_width, int(y))
        else:
            self.image_canvas.create_line(0, int(y), self.im_canv_width, int(y), dash=(4, 2))
        
    def determine_selection(self, xin, yin):
        min_index = -1
        min_distance = 1e30
        cur_index = 0
        for x in self.profile_points:
            current_distance = np.sqrt((x[0] - xin)**2 + (x[1] - yin)**2)
            if current_distance < min_distance:
                min_distance = current_distance
                min_index = cur_index
            cur_index = cur_index + 1
        if (min_distance / self.cur_ratio) < self.select_tolerance:
            self.selected_index = min_index
    
    def draw_marker(self, xin, yin, selected):
        x = (xin) * self.cur_ratio + self.current_delta_x
        y = (yin) * self.cur_ratio + self.current_delta_y
        if not selected:
            v = self.image_canvas.create_line(int(x), int(y - self.datum_marker_length), int(x), int(y + self.datum_marker_length), width = self.markerwidth)
            h = self.image_canvas.create_line(int(x - self.datum_marker_length), int(y), int(x + self.datum_marker_length), int(y), width = self.markerwidth)
        else:
            v = self.image_canvas.create_line(int(x), int(y - self.datum_marker_length), int(x), int(y + self.datum_marker_length), width = self.markerwidth, fill = "red")
            h = self.image_canvas.create_line(int(x - self.datum_marker_length), int(y), int(x + self.datum_marker_length), int(y), width = self.markerwidth, fill = "red")
        
    def on_b3_release_img(self, event):
        self.ini_m_x = -1
        self.ini_m_y = -1
    
    def on_b1_release_img(self, event):
        if not self.controldown:
            self.selected_index = -1
        self.refresh_all()
        self.ini_m_x_sel = -1
        self.ini_m_y_sel = -1
    def on_scroll_img(self, event):
        if self.has_image:
            sign_var = -1
            if sign_var*event.delta < 0:
                self.cur_ratio = self.cur_ratio * self.scroll_ratio
            else:
                self.cur_ratio = self.cur_ratio / self.scroll_ratio
            self.image_canvas.delete("all")
            new_height = int(self.cur_ratio * self.raw_image.height)
            new_width = int(self.cur_ratio * self.raw_image.width)
            image = self.raw_image.resize((new_width, new_height), pil_image.ANTIALIAS)
            photo = pil_imagetk.PhotoImage(image)
            photo.master = self.master
            self.image_on_canvas = photo
            self.curimg = self.image_canvas.create_image(0, 0, image=photo, anchor="nw")
            self.image_canvas.itemconfig(self.image_on_canvas, image = photo)
            self.image_canvas.move(self.curimg, self.current_delta_x, self.current_delta_y)
            self.refresh_all()
        
    def on_mouse1_drag_img(self, event):
        if self.has_image and self.selected_index >= 0:
            if self.ini_m_x_sel < 0:
                self.ini_m_x_sel = event.x
            if self.ini_m_y_sel < 0:
                self.ini_m_y_sel = event.y
            cx = event.x
            cy = event.y
            c_dx = cx - self.ini_m_x_sel;
            c_dy = cy - self.ini_m_y_sel;
            current_node = self.profile_points[self.selected_index]
            self.profile_points[self.selected_index] = (current_node[0] + c_dx / self.cur_ratio, current_node[1] + c_dy / self.cur_ratio)
            self.ini_m_x_sel = cx
            self.ini_m_y_sel = cy
            self.refresh_all()
    
    def on_mouse3_drag_img(self, event):
        if self.has_image:
            if self.ini_m_x < 0:
                self.ini_m_x = event.x
            if self.ini_m_y < 0:
                self.ini_m_y = event.y
            self.image_canvas.delete("all")
            photo = self.image_on_canvas
            self.curimg = self.image_canvas.create_image(0, 0, image=photo, anchor="nw")
            self.image_canvas.itemconfig(self.image_on_canvas, image = photo)
            cx = event.x
            cy = event.y
            self.image_canvas.move(self.curimg, self.current_delta_x, self.current_delta_y)
            self.current_delta_x = self.current_delta_x + cx - self.ini_m_x
            self.current_delta_y = self.current_delta_y + cy - self.ini_m_y
            self.ini_m_x = cx
            self.ini_m_y = cy
            self.refresh_all()
        
    def open_image_file(self):
        self.current_image_filename = tk_filedialog.askopenfilename(initialdir = ".",title = "Select file", filetypes = (("Images","*.jpg *.png"),("All files","*")))
        if (os.path.isfile(self.current_image_filename)):
            image = pil_image.open(self.current_image_filename)
            self.raw_image = image
            photo = pil_imagetk.PhotoImage(image)
            photo.master = self.master
            self.image_on_canvas = photo
            self.curimg = self.image_canvas.create_image(0, 0, image=photo, anchor="nw")
            self.image_canvas.itemconfig(self.image_on_canvas, image = photo)
            self.has_image = True

window = ProfileExtractWindow()
window.open_window()