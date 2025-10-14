# 🚀 YouTube Downloader Silver

<p>
Software para facilitar o download de vídeos do Youtube, sem propaganda e fácil de instalar.</p>

## **📋 Pré-requisitos do Sistema & Guia de Instalação**

- Python 3.8 ou superior instalado
- Arquivos do projeto: `baixar_youtube-v3-python.py` e `build_installer.py`

---

## **🔧 Processo de Criação do Instalador**

### **1. Preparação do Ambiente**

Estruture os arquivos em um diretório organizado:

```
H:\script-py-down-yt\
├── baixar_youtube-v3-python.py          ← Aplicação principal
└── build_installer.py                   ← Script de construção
```

### **2. Execução do Processo de Build**

Execute o arquivo:

```bash
build_installer.py
```

**Fluxo de Execução:**

```
1. Instalação automática de dependências (yt-dlp, pyinstaller, pillow)
2. Geração de ícone personalizado para o aplicativo
3. Compilação do executável standalone (.exe)
4. Criação dos scripts installer.bat e uninstaller.bat
5. Empacotamento final na pasta "YouTubeDownloader_Setup"
```

### **3. Tempo de Processamento**

⏱️ Duração estimada: 2-5 minutos

Indicadores de progresso:

```
✅ Dependências instaladas com sucesso
✅ Ícone personalizado criado
✅ Executável compilado
✅ Pacote de instalação gerado
```

### **4. Estrutura Final do Pacote**

Após conclusão, a estrutura será:

```
YouTubeDownloader_Setup\          ← PACOTE DE DISTRIBUIÇÃO
├── YouTubeDownloader.exe         ← Aplicativo compilado (20-30 MB)
├── installer.bat                 ← Script de instalação automática
├── uninstaller.bat               ← Script de remoção
└── README.txt                    ← Documentação do usuário
```

---

## **👤 Guia do Usuário Final**

### **Processo de Instalação**

#### **Etapa 1: Recebimento do Pacote**

- Acesse a pasta criada `YouTubeDownloader_Setup` se quiser copie essa pasta para guardar o programa, para futuras instalações;
- O usuário deve extrair o conteúdo em local acessível.

#### **Etapa 2: Instalação do Software**

1. Navegue até a pasta `YouTubeDownloader_Setup`
2. **Clique com botão direito** em `installer.bat`
3. Selecione **"Executar como administrador"**
4. Aguarde a confirmação de conclusão
5. Feche a janela do prompt

#### **Etapa 3: Utilização do Aplicativo**

- Um atalho será criado na Área de Trabalho: `YouTube Downloader`
- **Duplo clique** no ícone para iniciar
- Interface pronta para uso imediato

#### **Etapa 4: Remoção do Software**

1. Acesse a pasta original `YouTubeDownloader_Setup`
2. **Execute como administrador** o arquivo `uninstaller.bat`
3. Confirme a operação de remoção

---

## **⭐ Benefícios da Solução**

| Característica                        | Método Tradicional | Com Instalador |
| ------------------------------------- | ------------------ | -------------- |
| Requer Python                         | ✅ Necessário       | ❌ Eliminado    |
| Instalação de pacotes pip             | ✅ Manual           | ❌ Automatizada |
| Configuração de variáveis de ambiente | ✅ Complexa         | ❌ Simplificada |
| Conhecimento técnico necessário       | ✅ Avançado         | ❌ Básico       |
| Tamanho do pacote                     | ~5 MB              | ~30 MB         |
| Criação de atalhos                    | ❌ Manual           | ✅ Automática   |
| Processo de desinstalação             | ❌ Complexo         | ✅ Simplificado |

---

## **🔧 Configuração FFmpeg (Funcionalidade Avançada - Opcional)**

Para operação totalmente offline com conversão de áudio:

### **1. Download do FFmpeg**

```
https://github.com/BtbN/FFmpeg-Builds/releases
```

Baixe: `ffmpeg-master-latest-win64-gpl.zip`

### **2. Integração no Pacote**

```
YouTubeDownloader_Setup\
├── YouTubeDownloader.exe
├── ffmpeg.exe              ← Binário FFmpeg
├── ffprobe.exe             ← Binário FFprobe
├── installer.bat
└── ...
```

### **3. Atualização do Script de Instalação**

Inclua estas linhas após `copy /Y "YouTubeDownloader.exe"`:

```batch
if exist "ffmpeg.exe" copy /Y "ffmpeg.exe" "%INSTALL_DIR%\\ffmpeg.exe" >nul
if exist "ffprobe.exe" copy /Y "ffprobe.exe" "%INSTALL_DIR%\\ffprobe.exe" >nul
```

---

## **📊 Especificações Técnicas**

| Componente            | Tamanho Aproximado |
| --------------------- | ------------------ |
| YouTubeDownloader.exe | 25-35 MB           |
| ffmpeg.exe            | ~120 MB            |
| ffprobe.exe           | ~120 MB            |
| **Pacote básico**     | **~30 MB**         |
| **Pacote completo**   | **~270 MB**        |

---

## **🛠️ Resolução de Problemas**

### **Erro: "Python não encontrado" durante build**

```bash
# Verifique a instalação do Python
python --version

# Alternativa com caminho absoluto
C:\Python313\python.exe build_installer.py
```

### **Erro: "PyInstaller não disponível"**

```bash
pip install pyinstaller
```

### **Executável com tamanho excessivo (>100MB)**

```bash
# Aplicar compressão UPX
pip install pyinstaller[upx]
pyinstaller --upx-dir=upx ...
```

### **Problemas com execução de scripts .bat**

1. Clique com botão direito no arquivo
2. "Executar como administrador"
3. Autorize na solicitação de permissões

### **Bloqueio por software antivírus**

- Executáveis gerados podem ser detectados como falso-positivo
- Configure exceções no antivírus

---

## **🚀 Melhorias Futuras**

### **Instalador com Interface Gráfica**

```nsis
!include "MUI2.nsh"

Name "YouTube Downloader Silver"
OutFile "YouTubeDownloader_Setup.exe"
InstallDir "$PROGRAMFILES\YouTubeDownloader"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
```

### **Sistema de Atualização Automática**

Implementar verificação de versão e atualização automática.

### **Assinatura Digital**

Assinatura de código para evitar alertas do Windows:

```bash
signtool sign /f certificate.pfx /p password YouTubeDownloader.exe
```

### **Instalador Online**

Criador de instalador leve (~5MB) com download sob demanda.

---

## **🎯 Resumo**

**Processo Simplificado:**

```bash
python build_installer.py
```

**Resultado Obtido:**

- Pacote `YouTubeDownloader_Setup` pronto para distribuição
- Instalação automática via `installer.bat`
- Zero configurações manuais necessárias
- Compatibilidade total com Windows 10/11

---

## 🤝 Contribuindo

1. Faça um `fork` deste repositório

2. Crie uma branch:
   
   ```bash
   git checkout -b feature/nome-da-feature
   ```

3. Faça commits claros:
   
   ```bash
   git commit -m "feat: descrição da feature"
   ```

4. Faça push:
   
   ```bash
   git push origin feature/nome-da-feature
   ```

5. Abra um **Pull Request**

---

## 📝 Licença

Projeto sob licença **MIT**. Veja o arquivo [LICENSE](https://chatgpt.com/c/LICENSE) para detalhes.

---
