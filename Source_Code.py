#######sudo apt-get install libreoffice-core######
from kivy.config import Config
Config.set('graphics', 'resizable', False)
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.screen import Screen
import img2pdf
from pdf2image import convert_from_path
from PyPDF2 import PdfFileMerger, PdfFileWriter, PdfFileReader
import os
import pickle
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.dialog import MDDialog
import subprocess
import sys
from kivy.core.window import Window
import subprocess
from kivy.lang.builder import Builder
# Window.size=(400,500)

Builder.load_string("""
<HomeScreen>:
    name: "home_screen"
    MDScreen:
        md_bg_color:56/255,40/255,81/255,1
    MDBoxLayout:
        orientation:'vertical'
        MDBoxLayout:
            size_hint_y:.25
            padding:dp(25)
            MDBoxLayout:
                orientation:"vertical"
                MDLabel:
                    text:" Exotic PDF Converter"
                    font_style:"H4"
                MDBoxLayout:
                    adaptive_size:True
                    spacing:dp(10)
                    MDLabel:
                        text:" "
                        font_style:"H4"
                        text_size:None,None
                        adaptive_width:True
                    MDIcon:
                        icon:'home'
                    MDLabel:
                        text:"  Home"
                        font_style:"H6"
                        text_size:None,None
                        adaptive_width:True
                    

            MDIconButton:
                icon:"file-replace-outline"
                font_size : 48
                user_font_size: "64sp"
        MDGridLayout:
            size_hint_y:.9
            cols:3
            padding:[dp(15),dp(15),dp(15),dp(35)]
            spacing:dp(15)
            ElementCard:
                icons: "file-image-outline"
                text:"From PDF to image"
                on_press: 
                    root.manager.current = "pdf2imgscreen"   
                    root.manager.transition.direction = "left"
            ElementCard:
                icons: "file-document-outline"
                text:"From PDF to doc"
                on_press: 
                    root.manager.current = "pdf2docscreen"   
                    root.manager.transition.direction = "left"
            ElementCard:
                icons: "file-image"
                text:"From image to PDF"
                on_press: 
                    root.manager.current = "img2pdfscreen"   
                    root.manager.transition.direction = "left"
            ElementCard:
                icons: "microsoft-office"
                text:"From document to PDF"
                on_press: 
                    root.manager.current = "off2pdfscreen"   
                    root.manager.transition.direction = "left"


            ElementCard:
                icons: "chevron-triple-down"
                text:"Compress PDF"
                on_press: 
                    root.manager.current = 'PDF_compression_tool_screen'
                    root.manager.transition.direction = "left"


            ElementCard:
                icons: "lock-open-check-outline"
                text:"Encrypt/Decrypt PDF"
                on_press: 
                    root.manager.current = 'ed'
                    root.manager.transition.direction = "left"

            ElementCard:
                icons: "scissors-cutting"
                text:"Split into individual PDF files"
                on_press: 
                    root.manager.current = 'splitpdfscreen'   
                    root.manager.transition.direction = "left"
            ElementCard:
                icons: 'plus-circle-outline'
                text:"Merge PDF Files"
                on_press: 
                    root.manager.current = 'mergepdfscreen'   
                    root.manager.transition.direction = "left"
            ElementCard:
                icons: 'package-down'
                text:"Extract pages from PDF"
                on_press: 
                    root.manager.current = 'extpdfscreen'   
                    root.manager.transition.direction = "left"
            ElementCard:
                icons: "folder-open-outline"
                text:"Open output directory"
                on_press: 
                    root.dir()
            ElementCard:
                icons: "map-marker-question-outline"
                text:"About"
                on_press: 
                    root.manager.current = 'info'
                    root.manager.transition.direction = "left"

            ElementCard:
                icons: "cog"
                text:"Settings"
                on_press: 
                    root.manager.current = 'settings'
                    root.manager.transition.direction = "left"
                    root.dir_status()

<ElementCard@MDCard>:
    md_bg_color:69/255,55/255,86/255,1
    padding:dp(15)
    spacing:dp(15)
    radius:dp(25)
    ripple_behavior: True

    text:''
    subtext:''
    icons:''

    orientation:'vertical'
  
    MDBoxLayout:
        orientation:'vertical'
        MDLabel:
            text:root.subtext
        MDLabel:
            text:root.subtext
        MDLabel:
            text:root.subtext
        MDIcon:
            halign:"center"
            icon:root.icons
            font_size : 48
        MDLabel:
            text:root.subtext
        MDLabel:
            text:root.subtext
        MDLabel:
            text:root.subtext
        MDLabel:
            text:root.subtext
        MDLabel:
            text:root.subtext
        MDLabel:
            text:root.subtext
        MDLabel:
            text:root.subtext
        MDLabel:
            halign:"center"
            text:root.text
     
<SettingsScreen>:
    name: 'settings'
    canvas.before:
        Color:
            rgba: (56/255,40/255,81/255,1)
        Rectangle:
            size: root.width, root.height
            pos: self.pos
    MDIcon:
        font_size: 32
        icon: "cog"
        pos_hint: {'center_x':0.9,'center_y':0.9}
    MDLabel:        
        text: '         Settings'
        halign: 'center'
        pos_hint: {'center_x':0.48,'center_y':0.9}
        font_style: "H4"
    MDFillRoundFlatIconButton:
        md_bg_color:69/255,55/255,86/255,1
        font_style:"H6"
        id:back
        disabled: False
        text: 'Back'
        icon: "arrow-left-circle-outline"
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press: 
            root.manager.current = 'home_screen'   
            root.manager.transition.direction = "right"
    MDFillRoundFlatIconButton:
        md_bg_color:69/255,55/255,86/255,1
        font_style:"H5"
        id: chg
        icon: "folder-open-outline"
        text: "Change output directory"
        disabled: False
        pos_hint: {"center_x": .5, "center_y": .45}
        on_press: 
            dir_status.disabled = False 
            confirm.disabled= False
            chg.disabled= True
            back.disabled = True
        font_style: "H6"
    MDFillRoundFlatIconButton:
        md_bg_color:69/255,55/255,86/255,1
        icon: "check"
        font_style:"H5"
        id: confirm
        text: "Confirm"
        pos_hint: {"center_x": .5, "center_y": .55}
        on_press: root.check_dir()
        font_style: "H6"
    MDTextFieldRound: 
        normal_color: 192/255, 151/255, 240/255,1
        font_size: 20
        id: dir_status
        size_hint:(1, None)
        size_hint_x:None
        width:(300)
        text:""
        height: "30dp"
        halign: "center"
        pos_hint:{'center_x': 0.5, 'center_y': 0.65}

<OFF2PDFScreen>:
    name: 'off2pdfscreen'
    canvas.before:
        Color:
            rgba: (56/255,40/255,81/255,1)
        Rectangle:
            size: root.width, root.height
            pos: self.pos
    MDLabel:
        text: "Convert document(any format) to PDF"
        halign: 'center'
        font_style: "H6"
        pos_hint: {"center_x": .5, "center_y": .9}
    MDFillRoundFlatIconButton:
        md_bg_color:69/255,55/255,86/255,1
        text: 'Back'
        font_style: "H6"
        icon: "arrow-left-circle-outline"
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press: 
            root.manager.current = 'home_screen'   
            root.manager.transition.direction = "right"
    MDFillRoundFlatIconButton:
        md_bg_color:69/255,55/255,86/255,1
        icon: "folder-open"
        text: "Open output directory"
        pos_hint: {"center_x": .5, "center_y": .25}
        font_style: "H6"
        on_press: root.File_Browser()
    MDFillRoundFlatIconButton:
        icon: "folder-open-outline"
        md_bg_color:69/255,55/255,86/255,1
        text: "Choose file(s)"
        pos_hint: {"center_x": .5, "center_y": .5}
        on_press: 
            root.manager.current = 'chooser_off2pdf'
            root.manager.transition.direction = "left"
        font_style: "H6"
    MDFillRoundFlatIconButton:
        md_bg_color:69/255,55/255,86/255,1
        text: "Convert"
        icon: "restart"
        pos_hint: {"center_x": .5, "center_y": .6}
        on_press: root.converter()
        font_style: "H6" 
    MDLabel:
        id: file_tail
        text: ""
        halign: 'center'
        pos_hint: {"center_x": .5, "center_y": .41}
<IMG2PDFScreen>:
    name: 'img2pdfscreen'
    canvas.before:
        Color:
            rgba: (56/255,40/255,81/255,1)
        Rectangle:
            size: root.width, root.height
            pos: self.pos
    MDLabel:
        font_style: "H5"
        text: "Convert Image to PDF"
        halign: 'center'
        pos_hint: {"center_x": .5, "center_y": .9} 
    MDFillRoundFlatIconButton:
        md_bg_color:69/255,55/255,86/255,1
        text: 'Back'
        icon: "arrow-left-circle-outline"
        font_style: "H6"
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press: 
            root.manager.current = 'home_screen'   
            root.manager.transition.direction = "right"
    MDLabel:
        text: "Split into individual PDF files"
        halign: 'center'
        pos_hint: {"center_x": .47, "center_y": .33}
    MDCheckbox:
        size_hint: None, None
        size: "48dp", "48dp"
        pos_hint: {'center_x': .62, 'center_y': .33}
        on_active: root.splitter(*args)                 
    MDFillRoundFlatIconButton:
        md_bg_color:69/255,55/255,86/255,1
        icon: "folder-open"
        text: "Open output directory"
        pos_hint: {"center_x": .5, "center_y": .25}
        font_style: "H6"
        on_press: root.File_Browser()
    MDFillRoundFlatIconButton:
        md_bg_color:69/255,55/255,86/255,1
        icon: "folder-open-outline"
        text: "Choose file(s)"
        pos_hint: {"center_x": .5, "center_y": .5}
        on_press: 
            root.manager.current = 'chooser_img2pdf'
            root.manager.transition.direction = "left"
        font_style: "H6"
    MDTextFieldRound: 
        normal_color: 192/255, 151/255, 240/255,1
        id: input
        size_hint:(1, None)
        size_hint_x:None
        width:(100)
        text:"Output"
        height: "30dp"
        halign: "center"
        pos_hint:{'center_x': 0.66, 'center_y': 0.75}
    MDFillRoundFlatIconButton:
        md_bg_color:69/255,55/255,86/255,1
        text: "Convert"
        icon: "restart"
        pos_hint: {"center_x": .5, "center_y": .6}
        on_press: root.converter()
        font_style: "H6"  
    MDLabel:
        text: "Processed PDF file will be saved as " + input.text + ".pdf"
        halign: 'center'
        pos_hint: {"center_x": .5, "center_y": .68}
    MDLabel:
        text: "Specify the name of your file : "
        halign: 'center'
        pos_hint: {"center_x": .4, "center_y": .75}
        font_style: "H6"
    MDLabel:
        id: file_tail
        text: ""
        halign: 'center'
        pos_hint: {"center_x": .5, "center_y": .41}

    
            
<Check@MDCheckbox>:
    group: 'group'
    size_hint: None, None
    size: dp(48), dp(48)       
<SPLITPDFScreen>:
    name: 'spltpdfscreen'
    canvas.before:
        Color:
            rgba: (56/255,40/255,81/255,1)
        Rectangle:
            size: root.width, root.height
            pos: self.pos
    MDLabel:
        text: "Split into individual PDF files"
        font_style: "H5"
        halign: 'center'
        pos_hint: {"center_x": .5, "center_y": .9} 
    MDFillRoundFlatIconButton:
        md_bg_color:69/255,55/255,86/255,1
        text: 'Back'
        font_style: "H6"
        icon: "arrow-left-circle-outline"
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press: 
            root.manager.current = 'home_screen'   
            root.manager.transition.direction = "right"
    MDFillRoundFlatIconButton:
        md_bg_color:69/255,55/255,86/255,1
        icon: "folder-open"
        text: "Open output directory"
        pos_hint: {"center_x": .5, "center_y": .25}
        font_style: "H6"
        on_press: root.File_Browser()
        font_style: "H6"
        on_press: root.File_Browser()
    MDFillRoundFlatIconButton:
        icon: "folder-open-outline"
        text: "Choose file(s)"
        md_bg_color:69/255,55/255,86/255,1
        pos_hint: {"center_x": .5, "center_y": .5}
        on_press: 
            root.manager.current = 'chooser_pdfsplit'
            root.manager.transition.direction = "left"
        font_style: "H6"
    MDFillRoundFlatIconButton:
        text: "Split"
        icon: "scissors-cutting"
        md_bg_color:69/255,55/255,86/255,1
        pos_hint: {"center_x": .5, "center_y": .6}
        on_press: root.converter()
        font_style: "H6" 
    MDLabel:
        id: file_tail
        text: ""
        halign: 'center'
        pos_hint: {"center_x": .5, "center_y": .41}
<ChooserPDFSplitScreen>:
    name: 'chooser_pdfsplit'
    canvas.before:
        Color:
            rgba: (56/255,40/255,81/255,1)
        Rectangle:
            size: root.width, root.height
            pos: self.pos
    MDRectangleFlatIconButton:
        text: 'Back'
        icon: "arrow-left-circle-outline"
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1
        line_color: 1, 1, 1, 1
        icon_color: 1, 1, 1, 1
        pos_hint: {'center_x':0.07,'center_y':0.045}
        on_press: 
            root.selected(Chooser.selection)
            root.manager.current = 'splitpdfscreen'   
            root.manager.transition.direction = "right"
    BoxLayout:
        orientation: "vertical"
        size: root.width, root.height/1.5
        padding: 70
        spacing: 20
        FileChooserIconView:
            id: Chooser
            multiselect: True
            filters: ['*.pdf']


<PDF_Compression_tool_Screen>:
    name: 'PDF_compression_tool_screen'
    canvas.before:
        Color:
            rgba: (56/255,40/255,81/255,1)
        Rectangle:
            size: root.width, root.height
            pos: self.pos
    MDLabel:
        text: "  High Compression (Lower file size & quality)"
        halign: 'center'
        pos_hint: {"center_x": .47, "center_y": .8}
        font_style: "H6"
    MDLabel:
        text: "Med. Compression (Med. file size & quality)"
        halign: 'center'
        pos_hint: {"center_x": .47, "center_y": .7}
        font_style: "H6"
    MDLabel:
        text: "  Low Compression (Higher file size & quality)"
        halign: 'center'
        pos_hint: {"center_x": .47, "center_y": .6}
        font_style: "H6"
    Check:
        
        pos_hint: {'center_x': .75, 'center_y': .8}
        on_active: root.High(*args)

    Check:
        pos_hint: {'center_x': .75, 'center_y': .7}
        on_active: root.Med(*args)

    Check:
        pos_hint: {'center_x': .75, 'center_y': .6}
        on_active: root.Low(*args)
    MDIcon:
        font_size : 28
        icon:"chevron-triple-down"
        halign: 'center'
        pos_hint: {"center_x": .38, "center_y": .9}
    MDLabel:
        text: "PDF Compressor"
        font_style: 'H5'
        halign: 'center'
        pos_hint: {"center_x": .52, "center_y": .9}
    MDFillRoundFlatIconButton:
        
        md_bg_color:69/255,55/255,86/255,1
        text: 'Back'
        font_style: "H6"
        icon: "arrow-left-circle-outline"
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press: 
            root.manager.current = 'home_screen'   
            root.manager.transition.direction = "right"
    MDFillRoundFlatIconButton:
        md_bg_color:69/255,55/255,86/255,1
        icon: "folder-open"
        text: "Open output directory"
        pos_hint: {"center_x": .5, "center_y": .2}
        font_style: "H6"
        on_press: root.File_Browser()
    MDFillRoundFlatIconButton:
        md_bg_color:69/255,55/255,86/255,1
        icon: "folder-open-outline"
        text: "Choose file(s)"
        pos_hint: {"center_x": .5, "center_y": .4}
        on_press: 
            root.manager.current = 'chooser_CMPRS'
            root.manager.transition.direction = "left"
        font_style: "H6"
    MDFillRoundFlatIconButton:
        md_bg_color:69/255,55/255,86/255,1
        text: "Compress"
        icon: "chevron-triple-down"
        pos_hint: {"center_x": .5, "center_y": .5}
        on_press: root.converter()
        font_style: "H6" 
    MDLabel:
        id: file_tail
        text: ""
        halign: 'center'
        pos_hint: {"center_x": .5, "center_y": .323}
<Chooser_CMPRS>:
    name: 'chooser_CMPRS'
    canvas.before:
        Color:
            rgba: (56/255,40/255,81/255,1)
        Rectangle:
            size: root.width, root.height
            pos: self.pos
    MDRectangleFlatIconButton:
        text: 'Back'
        icon: "arrow-left-circle-outline"
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1
        line_color: 1, 1, 1, 1
        icon_color: 1, 1, 1, 1
        pos_hint: {'center_x':0.07,'center_y':0.045}
        on_press: 
            root.selected(Chooser.selection)
            root.manager.current = 'PDF_compression_tool_screen'   
            root.manager.transition.direction = 'right'
    BoxLayout:
        orientation: "vertical"
        size: root.width, root.height/1.5
        padding: 70
        spacing: 20
        FileChooserIconView:
            id: Chooser
            filters: ['*.pdf']
            multiselect: True









<ChooserScreenimg2pdf>:
    name:'chooser_img2pdf'   
    canvas.before:
        Color:
            rgba: (56/255,40/255,81/255,1)
        Rectangle:
            size: root.width, root.height
            pos: self.pos
    MDRectangleFlatIconButton:
        text: 'Back'
        icon: "arrow-left-circle-outline"
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1
        line_color: 1, 1, 1, 1
        icon_color: 1, 1, 1, 1
        pos_hint: {'center_x':0.07,'center_y':0.045}
        on_press: 
            root.selected(Chooser.selection)
            root.manager.current = 'img2pdfscreen'   
            root.manager.transition.direction = 'right'
    BoxLayout:
        orientation: "vertical"
        size: root.width, root.height/1.5
        padding: 70
        spacing: 20
        FileChooserIconView:
            id: Chooser
            filters: ['*.jpeg', '*.jpg', '*.png', '*.webp', '*.tiff', '*.gif']
            multiselect: True
<ChooserScreenOff2PDF>:
    name: 'chooser_off2pdf'
    canvas.before:
        Color:
            rgba: (56/255,40/255,81/255,1)
        Rectangle:
            size: root.width, root.height
            pos: self.pos
    MDRectangleFlatIconButton:
        text: 'Back'
        icon: "arrow-left-circle-outline"
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1
        line_color: 1, 1, 1, 1
        icon_color: 1, 1, 1, 1
        pos_hint: {'center_x':0.07,'center_y':0.045}
        on_press: 
            root.selected(Chooser.selection)
            root.manager.current = 'off2pdfscreen'   
            root.manager.transition.direction = "right"
    BoxLayout:
        orientation: "vertical"
        size: root.width, root.height/1.5
        padding: 70
        spacing: 20
        FileChooserIconView:
            id: Chooser
            multiselect: True
            filters: ['*.odp','*.otp','*.odg','*.fodp','*.uop','*.pptx','*.ppsx','*.potx','*.ppt','*.pps','*.pot','*.pptm','*.odt','*.ott','*.fodt','*.uot','*.docx','*.dotx','*.xml','*.doc','*.dot','*.html','*.rtf','*.txt','*.docm','*.ods','*.ots','*.fods','*.uos','*.xlsx','*.xltx','*.xls','*.xlt','*.dif','*.dbf','*.slk','*.csv','*.xlsm','*.otg','*.fodg']
<PDF2DOCScreen>:
    name: 'pdf2docscreen'
    canvas.before:
        Color:
            rgba: (56/255,40/255,81/255,1)
        Rectangle:
            size: root.width, root.height
            pos: self.pos
    MDLabel:
        text: "Convert PDF to doc"
        halign: 'center'
        font_style:"H5"
        pos_hint: {"center_x": .5, "center_y": .9} 
    MDFillRoundFlatIconButton:
        md_bg_color:69/255,55/255,86/255,1
        text: 'Back'
        font_style: "H6"
        icon: "arrow-left-circle-outline"
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press: 
            root.manager.current = 'home_screen'   
            root.manager.transition.direction = "right"
    MDFillRoundFlatIconButton:
        md_bg_color:69/255,55/255,86/255,1
        icon: "folder-open"
        text: "Open output directory"
        pos_hint: {"center_x": .5, "center_y": .25}
        font_style: "H6"
        on_press: root.File_Browser()
    MDFillRoundFlatIconButton:
        icon: "folder-open-outline"
        text: "Choose file(s)"
        md_bg_color:69/255,55/255,86/255,1
        pos_hint: {"center_x": .5, "center_y": .5}
        on_press: 
            root.manager.current = 'chooser_pdf2doc'
            root.manager.transition.direction = "left"
        font_style: "H6"
    MDFillRoundFlatIconButton:
        text: "Convert"
        icon: "restart"
        md_bg_color:69/255,55/255,86/255,1
        pos_hint: {"center_x": .5, "center_y": .6}
        on_press: root.converter()
        font_style: "H6" 
    MDLabel:
        id: file_tail
        text: ""
        halign: 'center'
        pos_hint: {"center_x": .5, "center_y": .41}
<CHOOSERPDF2DOC>:
    name: 'chooser_pdf2doc' 
    canvas.before:
        Color:
            rgba: (56/255,40/255,81/255,1)
        Rectangle:
            size: root.width, root.height
            pos: self.pos
    MDRectangleFlatIconButton:
        text: 'Back'
        icon: "arrow-left-circle-outline"
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1
        line_color: 1, 1, 1, 1
        icon_color: 1, 1, 1, 1
        pos_hint: {'center_x':0.07,'center_y':0.045}
        on_press: 
            root.selected(Chooser.selection)
            root.manager.current = 'pdf2docscreen'   
            root.manager.transition.direction = 'right'
    BoxLayout:
        orientation: "vertical"
        size: root.width, root.height/1.5
        padding: 70
        spacing: 20
        FileChooserIconView:
            id: Chooser
            filters: ['*pdf']
            multiselect: True
<PDF2IMGScreen>:
    name: 'pdf2imgscreen'
    canvas.before:
        Color:
            rgba: (56/255,40/255,81/255,1)
        Rectangle:
            size: root.width, root.height
            pos: self.pos
    MDLabel:
        text: "Convert PDF to image"
        halign: 'center'
        font_style: "H5"
        pos_hint: {"center_x": .5, "center_y": .9} 
    MDFillRoundFlatIconButton:
        md_bg_color:69/255,55/255,86/255,1
        text: 'Back'
        font_style: "H6"
        icon: "arrow-left-circle-outline"
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press: 
            root.manager.current = 'home_screen'   
            root.manager.transition.direction = "right"
    MDFillRoundFlatIconButton:
        md_bg_color:69/255,55/255,86/255,1
        icon: "folder-open"
        text: "Open output directory"
        pos_hint: {"center_x": .5, "center_y": .25}
        font_style: "H6"
        on_press: root.File_Browser()
    MDFillRoundFlatIconButton:
        md_bg_color:69/255,55/255,86/255,1
        icon: "folder-open-outline"
        text: "Choose file(s)"
        pos_hint: {"center_x": .5, "center_y": .5}
        on_press: 
            root.manager.current = 'chooser_pdf2img'
            root.manager.transition.direction = "left"
        font_style: "H6"
    MDFillRoundFlatIconButton:
        md_bg_color:69/255,55/255,86/255,1
        text: "Convert"
        icon: "restart"
        pos_hint: {"center_x": .5, "center_y": .6}
        on_press: root.converter()
        font_style: "H6" 
    MDLabel:
        id: file_tail
        text: ""
        halign: 'center'
        pos_hint: {"center_x": .5, "center_y": .41}
<ChooserPDF2IMG>:
    name: 'chooser_pdf2img'
    canvas.before:
        Color:
            rgba: (56/255,40/255,81/255,1)
        Rectangle:
            size: root.width, root.height
            pos: self.pos
    MDRectangleFlatIconButton:
        text: 'Back'
        icon: "arrow-left-circle-outline"
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1
        line_color: 1, 1, 1, 1
        icon_color: 1, 1, 1, 1
        pos_hint: {'center_x':0.07,'center_y':0.045}
        on_press: 
            root.selected(Chooser.selection)
            root.manager.current = 'pdf2imgscreen'   
            root.manager.transition.direction = "right"
    BoxLayout:
        orientation: "vertical"
        size: root.width, root.height/1.5
        padding: 70
        spacing: 20
        FileChooserIconView:
            id: Chooser
            multiselect: True
            filters: ['*.pdf'] 
<MrgPDFScreen>:
    name: 'mergepdfscreen'
    canvas.before:
        Color:
            rgba: (56/255,40/255,81/255,1)
        Rectangle:
            size: root.width, root.height
            pos: self.pos
    MDLabel:
        text: "Processed PDF file will be saved as " + input.text + ".pdf"
        halign: 'center'
        pos_hint: {"center_x": .5, "center_y": .68}
    
    MDLabel:
        font_style: "H5"
        text: "Merge/Concatenate PDF files"
        halign: 'center'
        pos_hint: {"center_x": .5, "center_y": .9}
    MDLabel:
        id: file_tail
        text: ""
        halign: 'center'
        pos_hint: {"center_x": .5, "center_y": .41}
    MDLabel:
        text: "Specify the name of your file : "
        halign: 'center'
        pos_hint: {"center_x": .4, "center_y": .75}
        font_style: "H6"
    MDTextFieldRound: 
        normal_color: 192/255, 151/255, 240/255,1
        id: input
        size_hint:(1, None)
        size_hint_x:None
        width:(100)
        text: "Output"
        height: "30dp"
        halign: "center"
        pos_hint:{'center_x': 0.66, 'center_y': 0.75}
    
    MDFillRoundFlatIconButton:
        md_bg_color:69/255,55/255,86/255,1
        text: 'Back'
        icon: "arrow-left-circle-outline"
        font_style: "H6"
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press: 
            root.manager.current = 'home_screen'   
            root.manager.transition.direction = "right"
    MDFillRoundFlatIconButton:
        md_bg_color:69/255,55/255,86/255,1
        icon: "folder-open"
        text: "Open output directory"
        pos_hint: {"center_x": .5, "center_y": .25}
        font_style: "H6"
        on_press: root.File_Browser()
    MDFillRoundFlatIconButton:
        md_bg_color:69/255,55/255,86/255,1
        icon: "folder-open-outline"
        text: "Choose file(s)"
        pos_hint: {"center_x": .5, "center_y": .5}
        on_press: 
            root.manager.current = 'chooser_mergepdf'
            root.manager.transition.direction = "left"
        font_style: "H6"
    MDFillRoundFlatIconButton:
        md_bg_color:69/255,55/255,86/255,1
        text: "Merge"
        icon: "plus-circle-outline"
        pos_hint: {"center_x": .5, "center_y": .6}
        on_press: root.converter()
        font_style: "H6" 
    
<Chooser_mergepdfscreen>:
    name: 'chooser_mergepdf'
    canvas.before:
        Color:
            rgba: (56/255,40/255,81/255,1)
        Rectangle:
            size: root.width, root.height
            pos: self.pos
    MDRectangleFlatIconButton:
        text: 'Back'
        icon: "arrow-left-circle-outline"
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1
        line_color: 1, 1, 1, 1
        icon_color: 1, 1, 1, 1
        pos_hint: {'center_x':0.07,'center_y':0.045}
        on_press: 
            root.selected(Chooser.selection)
            root.manager.current = 'mergepdfscreen'   
            root.manager.transition.direction = "right"
    BoxLayout:
        orientation: "vertical"
        size: root.width, root.height/1.5
        padding: 70
        spacing: 20
        FileChooserIconView:
            id: Chooser
            multiselect: True
            filters: ['*.pdf']     
<extractpagepdfScreen>:
    name: 'extpdfscreen'
    canvas.before:
        Color:
            rgba: (56/255,40/255,81/255,1)
        Rectangle:
            size: root.width, root.height
            pos: self.pos
    MDLabel:
        text: "Specify the name of your file : "
        halign: 'center'
        pos_hint: {"center_x": .4, "center_y": .7}
        font_style: "H6"
    MDTextFieldRound: 
        normal_color: 192/255, 151/255, 240/255,1
        id: input
        size_hint:(1, None)
        size_hint_x:None
        width:(100)
        text: "Output"
        height: "30dp"
        halign: "center"
        pos_hint:{'center_x': 0.66, 'center_y': 0.7}
    MDLabel:
        text: "From page"
        halign: 'center'
        pos_hint: {"center_x": .3, "center_y": .87} 
    MDLabel:
        text: "To page"
        halign: 'center'
        pos_hint: {"center_x": .66, "center_y": .87} 
    MDTextFieldRound: 
        id: input_end
        normal_color: 192/255, 151/255, 240/255,1
        input_filter: 'int'
        size_hint:(1, None)
        size_hint_x:None
        width:(50)
        text: "0"
        height: "30dp"
        halign: "center"
        pos_hint:{'center_x': 0.66, 'center_y': 0.8}
    MDTextFieldRound: 
        normal_color: 192/255, 151/255, 240/255,1
        id: input_start
        input_filter: 'int'
        size_hint:(1, None)
        size_hint_x:None
        width:(50)
        text: "0"
        height: "30dp"
        halign: "center"
        pos_hint:{'center_x': 0.3, 'center_y': 0.8}
    MDLabel:
        text: "Processed PDF file will be saved as " + input.text +"_subset_" + input_start.text + "-" + input_end.text + ".pdf"
        halign: 'center'
        pos_hint: {"center_x": .48, "center_y": .63}
    MDLabel:
        text: "Extract pages from your PDF file"
        font_style: "H5"
        halign: 'center'
        pos_hint: {"center_x": .5, "center_y": .95} 
    MDFillRoundFlatIconButton:
        font_style:"H6"
        md_bg_color:69/255,55/255,86/255,1
        text: 'Back'
        icon: "arrow-left-circle-outline"
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press: 
            root.manager.current = 'home_screen'   
            root.manager.transition.direction = "right"
    MDFillRoundFlatIconButton:
        icon: "folder-open"
        text: "Open output directory"
        md_bg_color:69/255,55/255,86/255,1
        pos_hint: {"center_x": .5, "center_y": .25}
        font_style: "H6"
        on_press: root.File_Browser()
    MDFillRoundFlatIconButton:
        md_bg_color:69/255,55/255,86/255,1
        icon: "folder-open-outline"
        text: "Choose file"
        pos_hint: {"center_x": .5, "center_y": .4}
        on_press: 
            root.manager.current = 'chooser_ext'
            root.manager.transition.direction = "left"
        font_style: "H6"
    MDFillRoundFlatIconButton:
        md_bg_color:69/255,55/255,86/255,1
        text: "Extract"
        icon: "package-down"
        pos_hint: {"center_x": .5, "center_y": .5}
        on_press: root.converter()
        font_style: "H6" 
    MDLabel:
        id: file_tail
        text: ""
        halign: 'center'
        pos_hint: {"center_x": .5, "center_y": .325}
<Chooser_extractpagepdf>:
    name: 'chooser_ext'
    canvas.before:
        Color:
            rgba: (56/255,40/255,81/255,1)
        Rectangle:
            size: root.width, root.height
            pos: self.pos
    MDRectangleFlatIconButton:
        text: 'Back'
        icon: "arrow-left-circle-outline"
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1
        line_color: 1, 1, 1, 1
        icon_color: 1, 1, 1, 1
        pos_hint: {'center_x':0.07,'center_y':0.045}
        on_press: 
            root.selected(Chooser.selection)
            root.manager.current = 'extpdfscreen'   
            root.manager.transition.direction = "right"
    BoxLayout:
        orientation: "vertical"
        size: root.width, root.height/1.5
        padding: 70
        spacing: 20
        FileChooserIconView:
            id: Chooser
            
            filters: ['*.pdf']
<ED_Screen>:
    name: 'ed'
    canvas.before:
        Color:
            rgba: (56/255,40/255,81/255,1)
        Rectangle:
            size: root.width, root.height
            pos: self.pos
    MDLabel:
        text: "Encrypt/Decrypt PDF File"
        font_style: "H5"
        halign: 'center'
        pos_hint: {"center_x": .5, "center_y": .9}
    MDFillRoundFlatIconButton:
        md_bg_color:69/255,55/255,86/255,1
        text: 'Back'
        font_style: "H6"
        icon: "arrow-left-circle-outline"
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press: 
            root.manager.current = 'home_screen'   
            root.manager.transition.direction = "right"
    MDFillRoundFlatIconButton:
        md_bg_color:69/255,55/255,86/255,1
        icon: "folder-open"
        text: "Open output directory"
        pos_hint: {"center_x": .5, "center_y": .25}
        font_style: "H6"
        on_press: root.File_Browser()
    MDFillRoundFlatIconButton:
        md_bg_color:69/255,55/255,86/255,1
        icon: "folder-open-outline"
        text: "Choose file"
        pos_hint: {"center_x": .5, "center_y": .4}
        on_press: 
            root.manager.current = 'chooser_ed'
            root.manager.transition.direction = "left"
        font_style: "H6"
    MDFillRoundFlatIconButton:
        md_bg_color:69/255,55/255,86/255,1
        text: "Encrypt"
        icon: "lock"
        pos_hint: {"center_x": .5, "center_y": .6}
        on_press: root.ert()
        font_style: "H6" 
    MDFillRoundFlatIconButton:
        md_bg_color:69/255,55/255,86/255,1
        text: "Decrypt"
        icon: "key-variant"
        pos_hint: {"center_x": .5, "center_y": .5}
        on_press: root.drt()
        font_style: "H6"
    MDLabel:
     
        text: "Type the password -->"
        font_style: 'H6'
        halign: 'center'
        pos_hint: {"center_x": .4, "center_y": .7}
    MDTextFieldRound: 
        normal_color: 192/255, 151/255, 240/255,1
        normal_color: 192/255, 151/255, 240/255,1
        font_size : 17.5
        id: input_l
        size_hint:(1, None)
        size_hint_x:None
        width:(100)
        text: ""
        height: "30dp"
        halign: "center"
        pos_hint:{'center_x': 0.62, 'center_y': 0.7}
    MDLabel:
        id: file_tail
        text: ""
        halign: 'center'
        pos_hint: {"center_x": .5, "center_y": .325}
<Chooser_ED>:
    name: 'chooser_ed'
    canvas.before:
        Color:
            rgba: (56/255,40/255,81/255,1)
        Rectangle:
            size: root.width, root.height
            pos: self.pos
    MDRectangleFlatIconButton:
        text: 'Back'
        icon: "arrow-left-circle-outline"
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1
        line_color: 1, 1, 1, 1
        icon_color: 1, 1, 1, 1
        pos_hint: {'center_x':0.07,'center_y':0.045}
        on_press: 
            root.selected(Chooser.selection)
            root.manager.current = 'ed'   
            root.manager.transition.direction = "right"
    BoxLayout:
        orientation: "vertical"
        size: root.width, root.height/1.5
        padding: 70
        spacing: 20
        FileChooserIconView:
            id: Chooser
            
            filters: ['*.pdf']
<Info_Screen>:
    name: "info"
    MDScreen:
        md_bg_color:56/255,40/255,81/255,1
    BoxLayout:
        orientation: "vertical"
        size: root.width, root.height/1.5
        padding: 70
        spacing: 20
        MDLabel:
            text:" Exotic PDF Converter"
            font_style:"H6"
            text: 'Hello! The creator of this software here! My name is Asif, I am currently fifteen, this was my first open source project written in python using the kivy and kivymd framework. Thank you for downloading my software (I put an enormous amount of effort into making this thing), really means the world to me :) '
            # halign: 'center'
            pos_hint: {'center_x':0.5,'center_y':0.7}
        MDLabel:
            text:" Exotic PDF Converter"
            font_style:"H5"
            text: 'If you want to suggest some improvements or report a bug, feel free to send an email: asiftanvir2006@gmail.com'
            halign: 'center'
            pos_hint: {'center_x':0.5,'center_y':0.5}
            
        
        MDFillRoundFlatIconButton:
            md_bg_color:69/255,55/255,86/255,1
            font_style: "H6"
            icon: "arrow-left-circle-outline"
            text: "Back to Home screen"
            pos_hint: {"center_x": .5, "center_y": .1}
            on_press: 
                root.manager.current = 'home_screen'
                root.manager.transition.direction = "right"

""")

# Window.size = (600, 500)
home_directory = str(os.path.expanduser('~'))
global PDF_CONVERTER_PATH
PDF_CONVERTER_PATH = home_directory + "/" + ".Exotic_PDF_Converter"
outputdir = home_directory + "/" + "Exotic_PDF_Output"
global split_pass
split_pass = "o_o"

try:
    os.chdir(PDF_CONVERTER_PATH)
except:
    os.mkdir(PDF_CONVERTER_PATH)
    os.chdir(PDF_CONVERTER_PATH)
    pickle.dump(str(outputdir), open("cachedir.dat",  "wb"))
try:
    os.chdir(outputdir)
except:
    os.mkdir(outputdir)


class HomeScreen(Screen):
    def dir_status(self):
        os.chdir(PDF_CONVERTER_PATH)
        path_str = pickle.load(open("cachedir.dat",  "rb"))
        self.manager.get_screen("settings").ids.dir_status.text =path_str
        self.manager.get_screen("settings").ids.confirm.disabled = True
        self.manager.get_screen("settings").ids.dir_status.disabled = True
    def dir(self):
        os.chdir(PDF_CONVERTER_PATH)
        Loaded_Dir = pickle.load(open("cachedir.dat", "rb"))
        subprocess.Popen(["xdg-open", Loaded_Dir])


class Merge_Split_PDF_Screen(Screen):
    pass


class PDF_Compression_tool_Screen(Screen):
    global option
    option = 'X'
    def High(self, checkbox, value):
        global option
        if value == True:
            option='High' 
            
        else:
            option = 'X'
    def Med(self, checkbox, value):
        global option
        if value == True:
            option='med'
            
        else:
            option = 'X'
    def Low(self, checkbox, value):
        global option
        if value == True:
            option='low'
            
        else:
            option = 'X'
           
    def converter(self):
        try:
            if cmprs_error == "Right":
                pass
            else:
                dialog = MDDialog(
                    text="Please Choose file(s)",
                    title="Info",
                    buttons=[
                        MDFlatButton(text="OK",
                                    on_press=lambda _: dialog.dismiss()),
                    ],
                )
                dialog.open()
                return 
        except:
            dialog = MDDialog(
                text="Please Choose file(s)",
                title="Info",
                buttons=[
                    MDFlatButton(text="OK", on_press=lambda _: dialog.dismiss()),
                ],
            )
            dialog.open()
            return
        for no in cmprs_files:
            alpha_TAIL = os.path.basename(no)
            if  os.path.isfile(no) == True:
                pass
            else:
                dialog = MDDialog(text=alpha_TAIL + " does not exist/has been moved", title="Info",
                    buttons=[
                        MDFlatButton(text="OK",
                            on_press=lambda _: dialog.dismiss()
                        ),
                    ],
                )
                dialog.open()
                return
        if option == 'High':
            v = 'screen'
        if option == 'med':
            v = 'ebook'
        if option == 'low':
            v = 'prepress'
        if option == "X":
            dialog = MDDialog(
                    text="Please choose a level of compression",
                    title="Info",
                    buttons=[
                        MDFlatButton(text="OK",
                                     on_press=lambda _: dialog.dismiss()),
                    ],
                )
            dialog.open()
            return
        os.chdir(PDF_CONVERTER_PATH)
        os.chdir(pickle.load(open("cachedir.dat",  "rb")))
        for n in cmprs_files:
            #print(n)
            g = os.path.basename(n)
            r = os.path.splitext(g)[0]
            
            a = "gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/" + v +" -dNOPAUSE -dQUIET -dBATCH -sOutputFile="+"\'"+r+"\'"+"_compressed.pdf " + "\'"+n + "\'"
            
            try:
            
                if os.system(a) != 0:
                    raise Exception('wrongcommand does not exist')
            except:
            
                dialog = MDDialog(
                    text="Encrypted files cannot be compressed! Please decrypt it before using this tool",
                    title="Info",
                    buttons=[
                        MDFlatButton(text="OK",
                                     on_press=lambda _: dialog.dismiss()),
                    ],
                )
                dialog.open()
                return()
        os.chdir(PDF_CONVERTER_PATH)
        dialog = MDDialog(
                    text="Compression finished!",
                    title="Info",
                    buttons=[
                        MDFlatButton(text="OK",
                                     on_press=lambda _: dialog.dismiss()),
                    ],
                )
        dialog.open()
        
    def File_Browser(self):
        os.chdir(PDF_CONVERTER_PATH)
        Loaded_Dir = pickle.load(open("cachedir.dat", "rb"))
        subprocess.Popen(["xdg-open", Loaded_Dir])



        
class Chooser_CMPRS(Screen):

    def selected(self, files):
        global cmprs_error
        if str(files) != "[]":
            cmprs_error = "Right"
        else:
            cmprs_error = "wrong"
        global cmprs_files
        cmprs_files = files
        
           
        os.chdir(PDF_CONVERTER_PATH)
        fz = open("testC.out", 'w')
        sys.stdout = fz
        z = cmprs_files
        for n in z:
            ok = os.path.basename(n) + " |"
            print(ok, end=' ')
        fz.close()
        file = open('testC.out', 'r')
        data = file.read()
        if str(files) != "[]":
            self.manager.get_screen(
                "PDF_compression_tool_screen"
            ).ids.file_tail.text = "Chosen files(s): |" + " " + data
        else:
             self.manager.get_screen(
                "PDF_compression_tool_screen"
            ).ids.file_tail.text = ""







class OFF2PDFScreen(Screen):
    def converter(self):
        try:
            if error_off2pdf == "Right":
                pass
            else:
                dialog = MDDialog(
                    text="Please Choose file(s)",
                    title="Info",
                    buttons=[
                        MDFlatButton(text="OK",
                                    on_press=lambda _: dialog.dismiss()),
                    ],
                )
                dialog.open()
                return 
        except:
            dialog = MDDialog(
                text="Please Choose file(s)",
                title="Info",
                buttons=[
                    MDFlatButton(text="OK", on_press=lambda _: dialog.dismiss()),
                ],
            )
            dialog.open()
            return
        Loaded_Dir = "\'" + str(pickle.load(open("cachedir.dat",  "rb"))) + "\'"
        
        for no in files_off2pdf:
            alpha_TAIL = os.path.basename(no)
            if  os.path.isfile(no) == True:
                pass
            else:
                dialog = MDDialog(text=alpha_TAIL + " does not exist/has been moved", title="Info",
                    buttons=[
                        MDFlatButton(text="OK",
                            on_press=lambda _: dialog.dismiss()
                        ),
                    ],
                )
                dialog.open()
                return
        for no in files_off2pdf:
                alpha = "\'" + str(no) + "\'"          
                cmd = "libreoffice --headless --convert-to pdf " + alpha + " --outdir " + Loaded_Dir
                try:    
                    os.system(cmd)
                except:
                    dialog = MDDialog(text="Encrypted files cannot be converted! Please decrypt it before using this tool", title="Info",
                        buttons=[
                            MDFlatButton(text="OK",
                                on_press=lambda _: dialog.dismiss()
                            ),
                        ],
                    )
                    dialog.open()

        dialog = MDDialog(text="Conversion Completed Successfully", title="Info",
            buttons=[
                MDFlatButton(text="OK",
                    on_press=lambda _: dialog.dismiss()
                ),
            ],
        )
        dialog.open()
    def File_Browser(self):
        os.chdir(PDF_CONVERTER_PATH)
        Loaded_Dir = pickle.load(open("cachedir.dat", "rb"))
        subprocess.Popen(["xdg-open", Loaded_Dir])


        


class IMG2PDFScreen(Screen):
    def splitter(self, checkbox, value):
        global split_pass
        if value == True:
            split_pass = "Do"
        else:
            split_pass = "X"

    def File_Browser(self):
        os.chdir(PDF_CONVERTER_PATH)
        Loaded_Dir = pickle.load(open("cachedir.dat", "rb"))
        subprocess.Popen(["xdg-open", Loaded_Dir])

    def converter(self):
        try:    
            try:
                if error_img2pdf == "Right":
                    pass
                else:
                    dialog = MDDialog(
                        text="Please Choose file(s)",
                        title="Info",
                        buttons=[
                            MDFlatButton(text="OK",
                                        on_press=lambda _: dialog.dismiss()),
                        ],
                    )
                    dialog.open()
                    return
            except:
                dialog = MDDialog(
                    text="Please Choose file(s)",
                    title="Info",
                    buttons=[
                        MDFlatButton(text="OK",
                                    on_press=lambda _: dialog.dismiss()),
                    ],
                )
                dialog.open()
                return
            for no in files_img2pdf:
                alpha_TAIL = os.path.basename(no)
                if os.path.isfile(no) == True:
                    pass
                else:
                    dialog = MDDialog(
                        text=alpha_TAIL + " does not exist/has been moved",
                        title="Info",
                        buttons=[
                            MDFlatButton(text="OK",
                                        on_press=lambda _: dialog.dismiss()),
                        ],
                    )
                    dialog.open()
                    return
            Loaded_Dir = pickle.load(open("cachedir.dat", "rb"))
            namevariable = str(self.ids.input.text) + ".pdf"
            file_operated = str(Loaded_Dir + "/" + namevariable)
            os.chdir(Loaded_Dir)
            with open(namevariable, "wb") as f:
                f.write(img2pdf.convert(files_img2pdf))
            os.chdir(PDF_CONVERTER_PATH)
            if split_pass == "Do":
                os.chdir(Loaded_Dir)
                pdf = PdfFileReader(file_operated)
                for page in range(pdf.getNumPages()):
                    pdf_writer = PdfFileWriter()
                    pdf_writer.addPage(pdf.getPage(page))
                    output_filename = '{}_page_{}.pdf'.format(
                        self.ids.input.text, page + 1)
                    with open(output_filename, 'wb') as out:
                        pdf_writer.write(out)
                os.remove(file_operated)
                os.chdir(PDF_CONVERTER_PATH)
            dialog = MDDialog(
                text="Conversion Completed Successfully",
                title="Info",
                buttons=[
                    MDFlatButton(text="OK", on_press=lambda _: dialog.dismiss()),
                ],
            )
            dialog.open()

        except:
            dialog = MDDialog(text="Encrypted files cannot be converted! Please decrypt it before using this tool", title="Info",
                buttons=[
                    MDFlatButton(text="OK",
                        on_press=lambda _: dialog.dismiss()
                    ),
                ],
            )
            dialog.open()
            

class ChooserScreenimg2pdf(Screen):
    def selected(self, files):
        global error_img2pdf
        if str(files) != '[]':
            error_img2pdf = "Right"
        else:
            error_img2pdf = "Wrong"  
        global files_img2pdf
        files_img2pdf = files
        #print(files_img2pdf)
        os.chdir(PDF_CONVERTER_PATH)
        fz = open("test1.out", 'w')
        sys.stdout = fz
        z = files_img2pdf
        for n in z:
            ok = os.path.basename(n) + " |"
            print(ok, end=' ')
        fz.close()
        file = open('test1.out', 'r')
        data = file.read()
        if str(files) != "[]":
            self.manager.get_screen(
                "img2pdfscreen"
            ).ids.file_tail.text = "Chosen files(s): |" + " " + data
        else:
             self.manager.get_screen(
                "img2pdfscreen"
            ).ids.file_tail.text = ""


class ChooserScreenOff2PDF(Screen):
    def selected(self, files):
        global error_off2pdf
        if str(files) != "[]":
            error_off2pdf = "Right"
        else:
            error_off2pdf = "Wrong"
        global files_off2pdf
        files_off2pdf = files
        os.chdir(PDF_CONVERTER_PATH)
        fz = open("test2.out", 'w')
        sys.stdout = fz
        z = files_off2pdf
        for n in z:
            ok = os.path.basename(n) + " |"
            print(ok, end=' ')
        fz.close()
        file = open('test2.out', 'r')
        data = file.read()
        if str(files) != "[]":
            self.manager.get_screen(
                "off2pdfscreen"
            ).ids.file_tail.text = "Chosen files(s): |" + " " + data
        else:
             self.manager.get_screen(
                "off2pdfscreen"
            ).ids.file_tail.text = ""

class PDF2DOCScreen(Screen):
    def converter(self):
        try:
            try:
                if error_PDF2DOC == "Right":
                    pass
                else:
                    dialog = MDDialog(
                            text="Please Choose file(s)",
                            title="Info",
                            buttons=[
                                MDFlatButton(text="OK",
                                            on_press=lambda _: dialog.dismiss()),
                            ],
                        )
                    dialog.open()
                    return 
            except:
                dialog = MDDialog(
                            text="Please Choose file(s)",
                            title="Info",
                            buttons=[
                                MDFlatButton(text="OK",
                                            on_press=lambda _: dialog.dismiss()),
                            ],
                        )
                dialog.open()
                return 
            for no in files_PDF2DOC:
                alpha_TAIL = os.path.basename(no)
                if  os.path.isfile(no) == True:
                    pass
                else:
                    dialog = MDDialog(text=alpha_TAIL + " does not exist/has been moved", title="Info",
                        buttons=[
                            MDFlatButton(text="OK",
                                on_press=lambda _: dialog.dismiss()
                            ),
                        ],
                    )
                    dialog.open()
                    return
            Loaded_Dir = "\'" + str(pickle.load(open("cachedir.dat",  "rb"))) + "\'"
            for e in files_PDF2DOC:
                os.chdir(PDF_CONVERTER_PATH)
                alpha = "\'" + str(e) + "\'"
                alpha_TAIL = os.path.basename(e)
                cmd = 'libreoffice --infilter="writer_pdf_import" --headless --convert-to odt ' + alpha + " --outdir " + Loaded_Dir
                os.system(cmd)
                os.chdir(str(pickle.load(open("cachedir.dat",  "rb"))))
                source = str(os.path.splitext(alpha_TAIL)[0]) + ".odt"
                dest = str(os.path.splitext(alpha_TAIL)[0]) + ".doc"
                os.rename(source, dest)
            os.chdir(PDF_CONVERTER_PATH)
            dialog = MDDialog(text="Conversion Completed Successfully", title="Info",
                buttons=[
                    MDFlatButton(text="OK",
                        on_press=lambda _: dialog.dismiss()
                    ),
                ],
            )
            dialog.open()
        except:
            dialog = MDDialog(text="Encrypted files cannot be converted! Please decrypt it before using this tool", title="Info",
                buttons=[
                    MDFlatButton(text="OK",
                        on_press=lambda _: dialog.dismiss()
                    ),
                ],
            )
            dialog.open()
    def File_Browser(self):
        os.chdir(PDF_CONVERTER_PATH)
        Loaded_Dir = pickle.load(open("cachedir.dat", "rb"))
        subprocess.Popen(["xdg-open", Loaded_Dir])
class SPLITPDFScreen(Screen):
    def converter(self):
        try:
            try:
                if error_pdfSPLIT == "Right":
                    pass
                else:
                    dialog = MDDialog(
                                text="Please Choose file(s)",
                                title="Info",
                                buttons=[
                                    MDFlatButton(text="OK",
                                                on_press=lambda _: dialog.dismiss()),
                                ],
                            )
                    dialog.open()
                    return 
            except:
                dialog = MDDialog(
                                text="Please Choose file(s)",
                                title="Info",
                                buttons=[
                                    MDFlatButton(text="OK",
                                                on_press=lambda _: dialog.dismiss()),
                                ],
                        )
                dialog.open()
                return 
            for no in file_PDFSPLIT:
                alpha_TAIL = os.path.basename(no)
                if  os.path.isfile(no) == True:
                    pass
                else:
                    dialog = MDDialog(text=alpha_TAIL + " does not exist/has been moved", title="Info",
                        buttons=[
                            MDFlatButton(text="OK",
                                on_press=lambda _: dialog.dismiss()
                            ),
                        ],
                    )
                    dialog.open()
                    return
            os.chdir(PDF_CONVERTER_PATH)
            Loaded_Dir = pickle.load(open("cachedir.dat", "rb"))
            for n in file_PDFSPLIT:
                os.chdir(Loaded_Dir)
                pdf = PdfFileReader(n)
                alpha_tail = str(os.path.basename(n))
                filename = str(os.path.splitext(alpha_tail)[0])
                
                for page in range(pdf.getNumPages()):
                    pdf_writer = PdfFileWriter()
                    pdf_writer.addPage(pdf.getPage(page))
                    output_filename = '{}_page_{}.pdf'.format(
                        filename, page + 1)
                    with open(output_filename, 'wb') as out:
                        pdf_writer.write(out)
            os.chdir(PDF_CONVERTER_PATH)
            dialog = MDDialog(text="Conversion Completed Successfully", title="Info",
                buttons=[
                    MDFlatButton(text="OK",
                        on_press=lambda _: dialog.dismiss()
                    ),
                ],
            )
            dialog.open()
        except:
           
            dialog = MDDialog(text="Encrypted files cannot be split! Please decrypt it before using this tool", title="Info",
                buttons=[
                    MDFlatButton(text="OK",
                        on_press=lambda _: dialog.dismiss()
                    ),
                ],
            )
            dialog.open()

    def File_Browser(self):
        os.chdir(PDF_CONVERTER_PATH)
        Loaded_Dir = pickle.load(open("cachedir.dat", "rb"))
        subprocess.Popen(["xdg-open", Loaded_Dir])
class MrgPDFScreen(Screen):
    def converter(self):
        try:
            try:
                if error_msg == 'Right':
                    pass
                else:
                    dialog = MDDialog(
                                text="Please Choose file(s)",
                                title="Info",
                                buttons=[
                                    MDFlatButton(text="OK",
                                                on_press=lambda _: dialog.dismiss()),
                                ],
                            )
                    dialog.open()
                    return 
            except:
                dialog = MDDialog(
                                text="Please Choose file(s)",
                                title="Info",
                                buttons=[
                                    MDFlatButton(text="OK",
                                                on_press=lambda _: dialog.dismiss()),
                                ],
                            )
                dialog.open()
                return 
            for no in files_mergepdf:
                alpha_TAIL = os.path.basename(no)
                if  os.path.isfile(no) == True:
                    pass
                else:
                    dialog = MDDialog(text=alpha_TAIL + " does not exist/has been moved", title="Info",
                        buttons=[
                            MDFlatButton(text="OK",
                                on_press=lambda _: dialog.dismiss()
                            ),
                        ],
                    )
                    dialog.open()
                    return
            os.chdir(PDF_CONVERTER_PATH)
            os.chdir(pickle.load(open("cachedir.dat",  "rb")))
            nameroot = self.ids.input.text + ".pdf"
            merger = PdfFileMerger()
            for n in files_mergepdf:
                merger.append(n)
            merger.write(nameroot)
            merger.close()
            os.chdir(PDF_CONVERTER_PATH)
            dialog = MDDialog(text="Merging Completed Successfully", title="Info",
                buttons=[
                    MDFlatButton(text="OK",
                        on_press=lambda _: dialog.dismiss()
                    ),
                ],
            )
            dialog.open()
        except:
            dialog = MDDialog(text="Encrypted files cannot be merged! Please decrypt it before using this tool", title="Info",
                buttons=[
                    MDFlatButton(text="OK",
                        on_press=lambda _: dialog.dismiss()
                    ),
                ],
            )
            dialog.open()
    def File_Browser(self):
        os.chdir(PDF_CONVERTER_PATH)
        Loaded_Dir = pickle.load(open("cachedir.dat", "rb"))
        subprocess.Popen(["xdg-open", Loaded_Dir])

        


class Chooser_mergepdfscreen(Screen):
    def selected(self, files):
        global error_msg
        if str(files) != '[]':
            error_msg = 'Right'
        else:
            error_msg = 'Wrong'
        global files_mergepdf
        files_mergepdf = files
        os.chdir(PDF_CONVERTER_PATH)
        fz = open("test6.out", 'w')
        sys.stdout = fz
        z = files_mergepdf
        for n in z:
            ok = os.path.basename(n) + " |"
            print(ok, end=' ')
        fz.close()
        file = open('test6.out', 'r')
        data = file.read()
        if str(files) != "[]":
            self.manager.get_screen(
                "mergepdfscreen"
            ).ids.file_tail.text = "Chosen files(s): |" + " " + data
        else:
             self.manager.get_screen(
                "mergepdfscreen"
            ).ids.file_tail.text = ""
        



class ChooserPDFSplitScreen(Screen):
    def selected(self, files):
        global error_pdfSPLIT
        if str(files) != "[]":
            error_pdfSPLIT = "Right"
        else:
            error_pdfSPLIT = "Wrong"
        global file_PDFSPLIT
        file_PDFSPLIT = files
        os.chdir(PDF_CONVERTER_PATH)
        fz = open("test5.out", 'w')
        sys.stdout = fz
        z = file_PDFSPLIT
        for n in z:
            ok = os.path.basename(n) + " |"
            print(ok, end=' ')
        fz.close()
        file = open('test5.out', 'r')
        data = file.read()
        if str(files) != "[]":
            self.manager.get_screen(
                "splitpdfscreen"
            ).ids.file_tail.text = "Chosen files(s): |" + " " + data
        else:
             self.manager.get_screen(
                "splitpdfscreen"
            ).ids.file_tail.text = ""


class CHOOSERPDF2DOC(Screen):
    def selected(self, files):
        global error_PDF2DOC
        if str(files) != '[]':
            error_PDF2DOC = 'Right'
        else:
            error_PDF2DOC = 'Wrong'
        global files_PDF2DOC
        files_PDF2DOC = files
        os.chdir(PDF_CONVERTER_PATH)
        fz = open("test3.out", 'w')
        sys.stdout = fz
        z = files_PDF2DOC
        for n in z:
            ok = os.path.basename(n) + " |"
            print(ok, end=' ')
        fz.close()
        file = open('test3.out', 'r')
        data = file.read()
        if str(files) != "[]":
            self.manager.get_screen(
                "pdf2docscreen"
            ).ids.file_tail.text = "Chosen files(s): |" + " " + data
        else:
             self.manager.get_screen(
                "pdf2docscreen"
            ).ids.file_tail.text = ""
class PDF2IMGScreen(Screen):
    def converter(self):
        try:
            try:
                if error_pdf2img == "Right":
                    pass
                else:
                    dialog = MDDialog(
                            text="Please Choose file(s)",
                            title="Info",
                            buttons=[
                                MDFlatButton(text="OK",
                                            on_press=lambda _: dialog.dismiss()),
                            ],
                        )
                    dialog.open()
                    return 
            except:
                dialog = MDDialog(
                            text="Please Choose file(s)",
                            title="Info",
                            buttons=[
                                MDFlatButton(text="OK",
                                            on_press=lambda _: dialog.dismiss()),
                            ],
                        )
                dialog.open()
                return 
            for no in files_pdf2img:
                alpha_TAIL = os.path.basename(no)
                if  os.path.isfile(no) == True:
                    pass
                else:
                    dialog = MDDialog(text=alpha_TAIL + " does not exist/has been moved", title="Info",
                        buttons=[
                            MDFlatButton(text="OK",
                                on_press=lambda _: dialog.dismiss()
                            ),
                        ],
                    )
                    dialog.open()
                    return
            os.chdir(PDF_CONVERTER_PATH) 
            os.chdir(pickle.load(open("cachedir.dat",  "rb")))
            for n in files_pdf2img:
                    alpha_TAIL = os.path.basename(n)
                    
                    pages = convert_from_path(n)
                    count = 1
                    for page in pages:
                        CFile = str(os.path.splitext(alpha_TAIL)[0]) + "_" + str(count) + ".jpg"
                        count = count + 1
                        page.save(CFile)
            dialog = MDDialog(text="Conversion Completed Successfully", title="Info",
                buttons=[
                    MDFlatButton(text="OK",
                        on_press=lambda _: dialog.dismiss()
                    ),
                ],
            )
            dialog.open()
            os.chdir(PDF_CONVERTER_PATH)
        except:
            dialog = MDDialog(text="Encrypted files cannot be converted! Please decrypt it before using this tool", title="Info",
                buttons=[
                    MDFlatButton(text="OK",
                        on_press=lambda _: dialog.dismiss()
                    ),
                ],
            )
            dialog.open()
    def File_Browser(self):
        os.chdir(PDF_CONVERTER_PATH)
        Loaded_Dir = pickle.load(open("cachedir.dat", "rb"))
        subprocess.Popen(["xdg-open", Loaded_Dir])
class ChooserPDF2IMG(Screen):
    def selected(self, files):
        global error_pdf2img
        if str(files) != '[]':
            error_pdf2img = 'Right'
        else:
            error_pdf2img = 'Wrong'
        global files_pdf2img
        files_pdf2img = files
        os.chdir(PDF_CONVERTER_PATH)
        fz = open("test4.out", 'w')
        sys.stdout = fz
        z = files_pdf2img
        for n in z:
            ok = os.path.basename(n) + " |"
            print(ok, end=' ')
        fz.close()
        file = open('test4.out', 'r')
        data = file.read()
        if str(files) != "[]":
            self.manager.get_screen(
                "pdf2imgscreen"
            ).ids.file_tail.text = "Chosen files(s): |" + " " + data
        else:
             self.manager.get_screen(
                "pdf2imgscreen"
            ).ids.file_tail.text = ""
class SettingsScreen(Screen):
    def check_dir(self):
        try:
            os.chdir(self.ids.dir_status.text)
            from PIL import Image
            img = Image.new("RGB", (800, 1280), (255, 255, 255))
            img.save("%delete%dummy%file%", "PNG")
            os.remove("%delete%dummy%file%")

            self.ids.confirm.disabled = True
            self.ids.dir_status.disabled = True
            self.ids.back.disabled = False
            self.ids.chg.disabled= False
            os.chdir(PDF_CONVERTER_PATH)
            pickle.dump(self.ids.dir_status.text, open("cachedir.dat", "wb"))

        except:
            dialog = MDDialog(
                        text="Please choose a valid directory",
                        title="Info",
                        buttons=[
                            MDFlatButton(text="OK",
                                        on_press=lambda _: dialog.dismiss()),
                        ],
                    )
            dialog.open()
            return 

class extractpagepdfScreen(Screen):
   
    def converter(self):
        
        s = int(self.ids.input_start.text) 
        e = int(self.ids.input_end.text)
        if s > e:
            e = s
            self.ids.input_end.text = str(s)
        if s == 0:
            self.ids.input_start.text = str(1)
        if e == 0:
            self.ids.input_end.text = str(1)
        if s > e:
            e = s
            self.ids.input_end.text = str(s)
        try:
            if error_ext == "Right":
                pass
            else:
                dialog = MDDialog(
                        text="Please Choose file(s)",
                        title="Info",
                        buttons=[
                            MDFlatButton(text="OK",
                                        on_press=lambda _: dialog.dismiss()),
                        ],
                    )
                dialog.open()
                return 
        except:
            dialog = MDDialog(
                        text="Please Choose file(s)",
                        title="Info",
                        buttons=[
                            MDFlatButton(text="OK",
                                        on_press=lambda _: dialog.dismiss()),
                        ],
                    )
            dialog.open()
            return 
        for no in files_ext:
            alpha_TAIL = os.path.basename(no)
            if  os.path.isfile(no) == True:
                pass
            else:
                dialog = MDDialog(text=alpha_TAIL + " does not exist/has been moved", title="Info",
                    buttons=[
                        MDFlatButton(text="OK",
                            on_press=lambda _: dialog.dismiss()
                        ),
                    ],
                )
                dialog.open()
                return
        os.chdir(PDF_CONVERTER_PATH)
        os.chdir(pickle.load(open("cachedir.dat",  "rb")))
        
        if s > 9999:
            dialog = MDDialog(
                        text="Page Range is too large!",
                        title="Info",
                        buttons=[
                            MDFlatButton(text="OK",
                                        on_press=lambda _: dialog.dismiss()),
                        ],
                        )
            dialog.open()
            return
        elif e > 9999:
            dialog = MDDialog(
                        text="Page Range is too large!",
                        title="Info",
                        buttons=[
                            MDFlatButton(text="OK",
                                        on_press=lambda _: dialog.dismiss()),
                        ],
                        )
            dialog.open()
            return
        else:
            pass

       

        a = [s-1,]
        for i in range(s,e):
            a = a + [i,]
        try:
            for n in files_ext:
                pdf = PdfFileReader(n)
                pdf_read = PdfFileReader(open(n,'rb'))
                Tot = pdf_read.getNumPages()
            if Tot < e:
                dialog = MDDialog(
                            text="Invalid Page Range!",
                            title="Info",
                            buttons=[
                                MDFlatButton(text="OK",
                                            on_press=lambda _: dialog.dismiss()),
                            ],
                            )
                dialog.open()
                os.chdir(PDF_CONVERTER_PATH)
                return 
   
        

            pages = a 
            pdfWriter = PdfFileWriter()
        
            for page_num in pages:
                pdfWriter.addPage(pdf.getPage(page_num))

            with open(self.ids.input.text + '_subset_' + self.ids.input_start.text + "-" + self.ids.input_end.text +  '.pdf', 'wb') as f:
                pdfWriter.write(f)
                f.close()
            dialog = MDDialog(
                        text="Extraction Completed Successfully",
                        title="Info",
                        buttons=[
                            MDFlatButton(text="OK",
                                        on_press=lambda _: dialog.dismiss()),
                        ],
                        )
            dialog.open()
            os.chdir(PDF_CONVERTER_PATH)
            return 
        except:
            dialog = MDDialog(
                        text="Encrypted files cannot be compressed! Please decrypt it before using this tool",
                        title="Info",
                        buttons=[
                            MDFlatButton(text="OK",
                                        on_press=lambda _: dialog.dismiss()),
                        ],
                        )
            dialog.open()
            os.chdir(PDF_CONVERTER_PATH)
            return 
    def File_Browser(self):
        os.chdir(PDF_CONVERTER_PATH)
        Loaded_Dir = pickle.load(open("cachedir.dat", "rb"))
        subprocess.Popen(["xdg-open", Loaded_Dir])
class ED_Screen(Screen):
    def ert(self):
        try:
            if ed_error == "rt":
                pass
            else:
                dialog = MDDialog(
                        text="Please Choose file(s)",
                        title="Info",
                        buttons=[
                            MDFlatButton(text="OK",
                                        on_press=lambda _: dialog.dismiss()),
                        ],
                    )
                dialog.open()
                return
        except:
            dialog = MDDialog(
                        text="Please Choose file(s)",
                        title="Info",
                        buttons=[
                            MDFlatButton(text="OK",
                                        on_press=lambda _: dialog.dismiss()),
                        ],
                    )
            dialog.open()
            return
        for no in ed_file:
            alpha_TAIL = os.path.basename(no)
            if  os.path.isfile(no) == True:
                pass
            else:
                dialog = MDDialog(text=alpha_TAIL + " does not exist/has been moved", title="Info",
                    buttons=[
                        MDFlatButton(text="OK",
                            on_press=lambda _: dialog.dismiss()
                        ),
                    ],
                )
                dialog.open()
                return
        if self.ids.input_l.text == "":
            dialog = MDDialog(text="Please enter a valid password", title="Info",
                    buttons=[
                        MDFlatButton(text="OK",
                            on_press=lambda _: dialog.dismiss()
                        ),
                    ],
                )
            dialog.open()
            return
        elif self.ids.input_l.text.isspace() == True:
            dialog = MDDialog(text="Please enter a valid password", title="Info",
                    buttons=[
                        MDFlatButton(text="OK",
                            on_press=lambda _: dialog.dismiss()
                        ),
                    ],
                )
            dialog.open()
            return
        else:
            pass
        os.chdir(PDF_CONVERTER_PATH)
        os.chdir(pickle.load(open("cachedir.dat",  "rb")))
        for n in ed_file:
            a = os.path.basename(n)
            def encrypt(file, password):
                pdf  = PdfFileReader(file)
                writer = PdfFileWriter()
                for n in range(pdf.getNumPages()):
                    page = pdf.getPage(n)
                    writer.addPage(page)

                writer.encrypt(password)

                with open("Protected_" +  a  ,  'wb') as OP:
                    writer.write(OP)
        
        try:
            encrypt(n, str(self.ids.input_l.text))
            dialog = MDDialog(text="Encryption finished", title="Info",
                    buttons=[
                        MDFlatButton(text="OK",
                            on_press=lambda _: dialog.dismiss()
                        ),
                    ],
                )
            dialog.open()
            os.chdir(PDF_CONVERTER_PATH)
            return
        except:
            dialog = MDDialog(text="File is already encrypted", title="Info",
                    buttons=[
                        MDFlatButton(text="OK",
                            on_press=lambda _: dialog.dismiss()
                        ),
                    ],
                )
            dialog.open()
            os.chdir(PDF_CONVERTER_PATH)
            return
    def drt(self):
        try:
            if ed_error == "rt":
                pass
            else:
                dialog = MDDialog(
                        text="Please Choose file(s)",
                        title="Info",
                        buttons=[
                            MDFlatButton(text="OK",
                                        on_press=lambda _: dialog.dismiss()),
                        ],
                    )
                dialog.open()
                return
        except:
            dialog = MDDialog(
                        text="Please Choose file(s)",
                        title="Info",
                        buttons=[
                            MDFlatButton(text="OK",
                                        on_press=lambda _: dialog.dismiss()),
                        ],
                    )
            dialog.open()
            return
        for no in ed_file:
            alpha_TAIL = os.path.basename(no)
            if  os.path.isfile(no) == True:
                pass
            else:
                dialog = MDDialog(text=alpha_TAIL + " does not exist/has been moved", title="Info",
                    buttons=[
                        MDFlatButton(text="OK",
                            on_press=lambda _: dialog.dismiss()
                        ),
                    ],
                )
                dialog.open()
                return
        if self.ids.input_l.text == "":
            dialog = MDDialog(text="Please enter a valid password", title="Info",
                    buttons=[
                        MDFlatButton(text="OK",
                            on_press=lambda _: dialog.dismiss()
                        ),
                    ],
                )
            dialog.open()
            return
        elif self.ids.input_l.text.isspace() == True:
            dialog = MDDialog(text="Please enter a valid password", title="Info",
                    buttons=[
                        MDFlatButton(text="OK",
                            on_press=lambda _: dialog.dismiss()
                        ),
                    ],
                )
            dialog.open()
            return
        else:
            pass
        os.chdir(PDF_CONVERTER_PATH)
        os.chdir(pickle.load(open("cachedir.dat",  "rb")))
        for n in ed_file:
            a = os.path.basename(n)
            def decrypt(file, password):
                pdf  = PdfFileReader(file)
                writer = PdfFileWriter()
                pdf.decrypt(password)
                for n in range(pdf.getNumPages()):
                    page = pdf.getPage(n)
                    writer.addPage(page)

                

                with open("Decrypted_" + a,  'wb') as OP:
                    writer.write(OP)
        
        try:
            decrypt(n, str(self.ids.input_l.text))
            dialog = MDDialog(text="Decryption finished", title="Info",
                    buttons=[
                        MDFlatButton(text="OK",
                            on_press=lambda _: dialog.dismiss()
                        ),
                    ],
                )
            dialog.open()
            os.chdir(PDF_CONVERTER_PATH)
            return
        except:
            dialog = MDDialog(text="Either the file is already decrypted or the password is incorrect", title="Info",
                    buttons=[
                        MDFlatButton(text="OK",
                            on_press=lambda _: dialog.dismiss()
                        ),
                    ],
                )
            dialog.open()
            os.chdir(PDF_CONVERTER_PATH)
            return


    def File_Browser(self):
        os.chdir(PDF_CONVERTER_PATH)
        Loaded_Dir = pickle.load(open("cachedir.dat", "rb"))
        subprocess.Popen(["xdg-open", Loaded_Dir])
class Chooser_ED(Screen):
    def selected(self, files):
        global ed_error
        if str(files) != "[]":
            ed_error = 'rt'
        else:
            ed_error = 'fw'
        global ed_file
        ed_file = files
        os.chdir(PDF_CONVERTER_PATH)
        fz = open("test_ed.out", 'w')
        sys.stdout = fz
        z = ed_file
        for n in z:
            ok = os.path.basename(n) + " |"
            print(ok, end=' ')
        fz.close()
        file = open('test_ed.out', 'r')
        data = file.read()
        if str(files) != "[]":
            self.manager.get_screen(
                "ed"
            ).ids.file_tail.text = "Chosen file: |" + " " + data
        else:
             self.manager.get_screen(
                "ed"
            ).ids.file_tail.text = ""
class Info_Screen(Screen):
    pass

        
class Chooser_extractpagepdf(Screen):
    def selected(self, files):
        global error_ext
        if str(files) != '[]':
            error_ext = 'Right'
        else:
            error_ext = 'Wrong'
        global files_ext
        files_ext = files
        os.chdir(PDF_CONVERTER_PATH)
        fz = open("test_i.out", 'w')
        sys.stdout = fz
        z = files_ext
        for n in z:
            ok = os.path.basename(n) + " |"
            print(ok, end=' ')
        fz.close()
        file = open('test_i.out', 'r')
        data = file.read()
        if str(files) != "[]":
            self.manager.get_screen(
                "extpdfscreen"
            ).ids.file_tail.text = "Chosen file: |" + " " + data
        else:
             self.manager.get_screen(
                "extpdfscreen"
            ).ids.file_tail.text = ""


class MyApp(MDApp):
    def build(self):
        self.icon="icon_exotic_pdf.png"
        self.title = 'PDF_Toolkit_Linux'
        self.theme_cls.theme_style = "Dark" 
        self.theme_cls.primary_palette="Pink"
    
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home_screen'))
       
        sm.add_widget(Merge_Split_PDF_Screen(name='merge_split_PDF_screen'))
        sm.add_widget(
            PDF_Compression_tool_Screen(name='PDF_compression_tool_screen'))
        sm.add_widget(OFF2PDFScreen(name='off2pdfscreen'))
        sm.add_widget(IMG2PDFScreen(name='img2pdfscreen'))
        sm.add_widget(ChooserScreenimg2pdf(name='chooser_img2pdf'))
        sm.add_widget(ChooserScreenOff2PDF(name='chooser_off2pdf'))
        sm.add_widget(PDF2DOCScreen(name='pdf2docscreen'))
        sm.add_widget(CHOOSERPDF2DOC(name='chooser_pdf2doc'))
        sm.add_widget(PDF2IMGScreen(name='pdf2imgscreen'))
        sm.add_widget(ChooserPDF2IMG(name='chooser_pdf2img'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(SPLITPDFScreen(name='splitpdfscreen'))
        sm.add_widget(ChooserPDFSplitScreen(name = 'chooser_pdfsplit'))
        sm.add_widget(MrgPDFScreen(name = 'mergepdfscreen'))
        sm.add_widget(Chooser_mergepdfscreen(name = 'chooser_mergepdf'))
        sm.add_widget(extractpagepdfScreen(name = 'extpdfscreen'))
        sm.add_widget(Chooser_extractpagepdf(name = 'chooser_ext'))
        sm.add_widget(Chooser_CMPRS(name = 'chooser_CMPRS'))
        sm.add_widget(ED_Screen(name = 'ed'))
        sm.add_widget(Chooser_ED(name = 'chooser_ed'))
        sm.add_widget(Info_Screen(name = 'info'))
        #sm.add_widget(ChooserScreen(name='chooser_screen'))
        return sm


if __name__ == '__main__':
    MyApp().run()
