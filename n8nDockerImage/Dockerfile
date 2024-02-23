# Use a imagem oficial do Node.js como base
FROM node:14

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo package.json e package-lock.json para o diretório de trabalho
COPY package*.json ./

# Instale as dependências do n8n
RUN npm install

# Copie o código-fonte do n8n para o diretório de trabalho
COPY . .

# Exponha a porta em que o n8n será executado (padrão: 5678)
EXPOSE 5678

# Inicialize o n8n quando o contêiner for iniciado
CMD ["npm", "start"]
