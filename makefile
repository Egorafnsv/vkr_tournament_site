run:
	docker run --rm -p 8000:8000 -d -v trmnt-db:/app --name trnmt-site egorafnsv/manage-tournament-site:new
rund:
	docker run --rm -p 8000:8000 -d -v D:/Afanasov/vkr/tournament:/app --name trnmt-site egorafnsv/manage-tournament-site:new
stop:
	docker stop trnmt-site