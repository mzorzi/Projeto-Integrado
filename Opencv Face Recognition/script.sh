#!/bin/bash
echo "Deseja treinar o modelo?"
echo "1-SIM"
echo "2-NAO"

read opcao_escolhida1

if [ $opcao_escolhida1 == "1" ];
then
    echo "Iniciando conversão das fotos..."
    python3.6 extract_embeddings.py --dataset dataset --embeddings output/embeddings.pickle --detector face_detection_model --embedding-model openface_nn4.small2.v1.t7 

    echo "Treinando o modelo..."
    python3.6 train_model.py --embeddings output/embeddings.pickle --recognizer output/recognizer.pickle --le output/le.pickle 
    
else
    echo "Usando ultimo modelo"

fi


echo "Deseja testar em:"
echo "1-IMAGEM"
echo "2-VIDEO"

read opcao_escolhida

if [ $opcao_escolhida == "1" ];
then
    echo "Fazendo reconhecimento em imagem..."
    echo "Usando imagem: mumamaettvic.jpg"
    python3.6 recognize.py --detector face_detection_model --embedding-model openface_nn4.small2.v1.t7 --recognizer output/recognizer.pickle --le output/le.pickle --image images/mumamaettvic.jpg 
elif [ $opcao_escolhida == "2" ];
    then
        echo "Fazendo reconhecimento em video..."
        python3.6 recognize_video.py --detector face_detection_model --embedding-model openface_nn4.small2.v1.t7 --recognizer output/recognizer.pickle --le output/le.pickle 
else
    echo "Opcao invalida!"

fi

