from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import os
from typing import Optional

from data_reader import read_z_values, get_data_dir, get_output_dir
from text_processor import assign_boldness
from random_boldness import assign_boldness_random
from vertical_invert_boldness import assign_boldness_vertical_inverted
from vertical_invert_chaotic import assign_boldness_vertical_chaotic
from image_generator import generate_image
from svg_generator import generate_svg


class PulsarifyGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Pulsarify GUI')
        self.resize(900, 700)
        self._build_ui()

    def _build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        inp_group = QtWidgets.QGroupBox('Input')
        inp_layout = QtWidgets.QHBoxLayout()
        self.text_edit = QtWidgets.QPlainTextEdit()
        self.text_edit.setPlaceholderText('Введите текст или нажмите "Open" для загрузки файла...')
        inp_layout.addWidget(self.text_edit)

        file_vbox = QtWidgets.QVBoxLayout()
        self.open_btn = QtWidgets.QPushButton('Open File')
        self.open_btn.clicked.connect(self.open_file)
        file_vbox.addWidget(self.open_btn)

        self.load_example_btn = QtWidgets.QPushButton('Load example from data/input.txt')
        self.load_example_btn.clicked.connect(self.load_example)
        file_vbox.addWidget(self.load_example_btn)

        file_vbox.addStretch()
        inp_layout.addLayout(file_vbox)
        inp_group.setLayout(inp_layout)
        layout.addWidget(inp_group)

        gen_group = QtWidgets.QGroupBox('Generator')
        gen_layout = QtWidgets.QFormLayout()

        self.generator_combo = QtWidgets.QComboBox()
        self.generator_combo.addItems([
            '1 - Deterministic (from pulsar values)',
            '2 - Random per-character',
            '3 - Vertical inversion (columns)',
            '4 - Vertical inversion + chaos'
        ])
        gen_layout.addRow('Generator', self.generator_combo)

        self.seed_edit = QtWidgets.QLineEdit()
        self.seed_edit.setPlaceholderText('целое число или пусто')
        gen_layout.addRow('Seed (int)', self.seed_edit)

        self.chaos_edit = QtWidgets.QLineEdit()
        self.chaos_edit.setPlaceholderText('0.0 - 2.0 (только для генератора 4)')
        gen_layout.addRow('Chaos (for gen 4)', self.chaos_edit)

        gen_group.setLayout(gen_layout)
        layout.addWidget(gen_group)


        out_group = QtWidgets.QGroupBox('Output')
        out_layout = QtWidgets.QFormLayout()

        self.format_combo = QtWidgets.QComboBox()
        self.format_combo.addItems(['png', 'svg'])
        out_layout.addRow('Format', self.format_combo)

        self.outpath_edit = QtWidgets.QLineEdit('output')
        out_layout.addRow('Output basename', self.outpath_edit)

        out_group.setLayout(out_layout)
        layout.addWidget(out_group)

        bottom_h = QtWidgets.QHBoxLayout()
        self.status_label = QtWidgets.QLabel('Ready')
        bottom_h.addWidget(self.status_label)
        bottom_h.addStretch()
        self.generate_btn = QtWidgets.QPushButton('Generate')
        self.generate_btn.clicked.connect(self.generate)
        bottom_h.addWidget(self.generate_btn)
        layout.addLayout(bottom_h)

    def open_file(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open text file', os.getcwd(), 'Text Files (*.txt);;All Files (*)')
        if not path:
            return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
            self.text_edit.setPlainText(text)
            self.status_label.setText(f'Loaded: {os.path.basename(path)}')
        except Exception as e:
            self.status_label.setText(f'Error loading file: {e}')

    def load_example(self):
        try:
            text = read_z_values()  
        except Exception:
            
            p = os.path.join('data', 'input.txt')
            try:
                with open(p, 'r', encoding='utf-8') as f:
                    text = f.read()
            except Exception as e:
                self.status_label.setText(f'Cannot load example: {e}')
                return
        
        try:
            data_dir = get_data_dir()
            p = os.path.join(data_dir, 'input.txt')
            with open(p, 'r', encoding='utf-8') as f:
                data_text = f.read()
            self.text_edit.setPlainText(data_text)
            self.status_label.setText('Loaded data/input.txt')
        except Exception as e:
            self.status_label.setText(f'Cannot load example: {e}')

    def _parse_seed(self) -> Optional[int]:
        s = self.seed_edit.text().strip()
        if not s:
            return None
        try:
            return int(s)
        except Exception:
            return None

    def _parse_chaos(self) -> float:
        s = self.chaos_edit.text().strip()
        if not s:
            return 0.5
        try:
            return float(s)
        except Exception:
            return 0.5

    def generate(self):
        text = self.text_edit.toPlainText()
        if not text:
            self.status_label.setText('Please provide input text')
            return

        gen_index = self.generator_combo.currentIndex() + 1
        seed = self._parse_seed()
        chaos = self._parse_chaos()

        
        z_values = None
        try:
            z_values = read_z_values()
        except Exception:
            z_values = None

        try:
            if gen_index == 2:
                groups = assign_boldness_random(text, seed=seed)
            elif gen_index == 3:
                if z_values is None:
                    self.status_label.setText('cp1919.csv not found for generator 3')
                    return
                groups = assign_boldness_vertical_inverted(text, z_values)
            elif gen_index == 4:
                if z_values is None:
                    self.status_label.setText('cp1919.csv not found for generator 4')
                    return
                groups = assign_boldness_vertical_chaotic(text, z_values, seed=seed, chaos=chaos)
            else:
                if z_values is None:
                    self.status_label.setText('cp1919.csv not found for generator 1')
                    return
                groups = assign_boldness(text, z_values)
        except Exception as e:
            self.status_label.setText(f'Error during generation: {e}')
            return

        data_dir = get_data_dir()
        font_dir = os.path.join(data_dir, '11zon_zip')
        fmt = self.format_combo.currentText()
        out_basename = self.outpath_edit.text().strip() or 'output'
        try:
            out_dir = get_output_dir()
            if fmt == 'svg':
                out_path = os.path.join(out_dir, out_basename if out_basename.lower().endswith('.svg') else out_basename + '.svg')
                generate_svg(groups, font_dir, out_path)
            else:
                image = generate_image(groups, font_dir)
                out_path = os.path.join(out_dir, out_basename if out_basename.lower().endswith('.png') else out_basename + '.png')
                image.save(out_path)
            self.status_label.setText(f'Generated: {out_path}')
        except Exception as e:
            self.status_label.setText(f'Error saving output: {e}')


def run_app():
    app = QtWidgets.QApplication(sys.argv)
    gui = PulsarifyGUI()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run_app()
